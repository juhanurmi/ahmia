onion_counter = {}

db.onions.find().forEach(
    function(onion) {
        if(onion.domain in onion_counter){
            if( onion_counter[onion.domain] > 10 ) {
                //db.onions.remove({_id:onion.id});
                //print( "onions > 10" );
                }
            else {
                onion_counter[onion.domain] = onion_counter[onion.domain] + 1;
                print( "Domain: " + onion.domain );
                db.getSiblingDB('sample_data')['onions'].insert(onion);
                }
            }
        else {
            onion_counter[onion.domain] = 1;
            print( "Domain: " + onion.domain );
            db.getSiblingDB('sample_data')['onions'].insert(onion);
            }
        }
);
