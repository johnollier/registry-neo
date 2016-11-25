import csv

register='local-authority-type'
#register='local-authority-eng'
register_state_label = register.replace('-','_') + '_state'

tsv_file_name = '{0}/{0}.tsv'.format(register)
entity_file_name = '{0}/{0}-entity.csv'.format(register)
state_file_name = '{0}/{0}-state.csv'.format(register)
rel_file_name = '{0}/{0}-rel.csv'.format(register)

#fields = [ 'local-authority-eng','local-authority-type','name','official-name','start-date','end-date']
time_fields = ['end-date','start-date']
link_fields = []
#link_fields = ['local-authority-type']
non_state_fields = time_fields + link_fields 
entity_fields = ['public_id:ID']
rel_fields = [':START_ID',':END_ID','from','to','entry_number','created',':LABEL']

with open(tsv_file_name, newline='') as csvfile:
     reader = csv.reader(csvfile, delimiter='\t')
     fields = list(next( reader ))

state_fields = [f for f in fields if f not in non_state_fields] + [ register_state_label ]
print( state_fields )

entity_file = open(entity_file_name, 'w')
entity_writer = csv.DictWriter(entity_file, fieldnames=entity_fields)
entity_writer.writeheader()

state_file = open(state_file_name,'w')
state_writer = csv.DictWriter(state_file, fieldnames = state_fields)
state_writer.writeheader()

rel_file = open(rel_file_name,'w')
rel_writer = csv.DictWriter(rel_file, fieldnames=rel_fields)
rel_writer.writeheader()

with open(tsv_file_name, newline='') as csvfile:
     entry_number = 1
     reader = csv.DictReader(csvfile, delimiter='\t')
     for row in reader:
        entity_id = row[register]
        entity_map = {'public_id:ID' : entity_id }
        entity_writer.writerow( entity_map)
        # state
        state_map = { k:v for (k,v) in row.items() if k not in non_state_fields}
        state_map[ register_state_label ] = entity_id + '0'
        state_writer.writerow( state_map )
        # relationships 
        state_rel = {':START_ID':entity_id,':END_ID':entity_id+'0','from':1,'to':4000000,
                'entry_number':entry_number,'created':3000000,':LABEL':'STATE'}
        rel_writer.writerow(state_rel)
        entry_number += 1        
        for link_field in link_fields:
            link_rel = {':START_ID':entity_id,':END_ID': row[ link_field ],'from':1,'to':4000000,'entry_number':entry_number,
                'created':3000000,':LABEL':'local_authority_type'}
            rel_writer.writerow(link_rel)
            entry_number += 1        

        
entity_file.close()
state_file.close()
rel_file.close()


