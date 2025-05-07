# Airbnb Booking Insights Dashboard
📊 A Streamlit-powered interactive dashboard that provides insights into Airbnb listings, helping users make informed booking decisions through data visualization.

🚀 Features <br>
✔️ Listings Overview: Explore Airbnb listings by location, room type, and availability. <br>
✔️ Detailed Insights: Filter listings based on country, neighborhood, price, cancellation policy, and more. <br>
✔️ Comparative Analysis: Identify top locations with the highest prices, most reviews, and different room types. <br>
✔️ Visualizations:

Bar Charts: Availability distribution, top neighborhoods.

Pie Charts: Room type distribution, instant bookable listings.

Histograms: Price and review distributions.

Line Graphs: Trends in Airbnb reviews over time.

📂 Dataset <br>
Uses Airbnb_Open_Data.csv for analysis.



APEX Trigger

trigger studentTrigger on student__c (after insert) {
    // Get all recruiters
        List<recruiter__c> recruiters = [SELECT Id, specialization__c, domain__c FROM recruiter__c];
    
    List<student__c> toUpdate = new List<student__c>();

    for (student__c cand : Trigger.new) {
        for (recruiter__c rec : recruiters) {
            if (cand.specialization__c == rec.specialization__c &&
                cand.domain__c == rec.domain__c) {
                
                // Prepare the updated candidate with assigned recruiter
                toUpdate.add(new student__c(
                    Id = cand.Id,
                    recruiter__c = rec.Id
                ));
                break; // Stop once a match is found
            }
        }
    }

    if (!toUpdate.isEmpty()) {
        update toUpdate;
    }
}

APEX Class

PUBLIC CLASS INVENTORY {

    //FUNCTION TO INSERT ITEMS
    PUBLIC STATIC VOID INSERTINVENTORYITEMS() {
        // CREATE A LIST TO HOLD PRODUCT__C RECORDS
        LIST<PRODUCT__C> ITEMLIST = NEW LIST<PRODUCT__C>();

        // CREATE NEW PRODUCT__C RECORDS
        PRODUCT__C ITEM2 = NEW PRODUCT__C(
            NAME = 'MACBOOK',
            QUANTITY__C = 10,
            PRICE__C = 20,
            DESCRIPTION__C = 'TEST 1',
            INVENTORY__C = 'A07DL00000W6YW0QAN'
        );

        // ADD THE RECORDS TO THE LIST
        ITEMLIST.ADD(ITEM2);
        
        // INSERT THE LIST OF RECORDS
        TRY {
            INSERT ITEMLIST;
            SYSTEM.DEBUG('ITEMS INSERTED SUCCESSFULLY.');
        } CATCH (DMLEXCEPTION E) {
            SYSTEM.DEBUG('ERROR INSERTING ITEMS: ' + E.GETMESSAGE());
        }
    }


    
    //FUNCTION TO UPDATE ITEMS
    PUBLIC STATIC VOID UPDATEINVENTORYITEMS() {
        // QUERY AN EXISTING RECORD (MAKE SURE THIS ID EXISTS IN YOUR ORG)
        LIST<PRODUCT__C> OWNERSTOUPDATE = [
            SELECT ID, NAME,QUANTITY__C, PRICE__C , DESCRIPTION__C , INVENTORY__C
            FROM PRODUCT__C 
            WHERE NAME = 'RAJAT'
            LIMIT 1
        ];

        IF (!OWNERSTOUPDATE.ISEMPTY()) {
            PRODUCT__C PROD = OWNERSTOUPDATE[0];
            PROD.NAME = 'AVANEESH';
            PROD.PRICE__C = 4000;
            PROD.DESCRIPTION__C = 'PRODUCT UPDATED';

            TRY {
                UPDATE PROD;
                SYSTEM.DEBUG('PRODUCT UPDATED SUCCESSFULLY.');
            } CATCH (DMLEXCEPTION E) {
                SYSTEM.DEBUG('ERROR UPDATING PRODUCT : ' + E.GETMESSAGE());
            }
        } ELSE {
            SYSTEM.DEBUG('NO MATCHING PRODUCT FOUND TO UPDATE.');
        }
    }
    
    //FUNCTION TO DELETE ITEMS
     PUBLIC STATIC VOID DELETEINVENTORYITEMS() {
        // QUERY AN EXISTING PRODUCT__C RECORD
        LIST<PRODUCT__C> PRODSTODELETE = [
            SELECT ID, NAME,QUANTITY__C, PRICE__C , DESCRIPTION__C , INVENTORY__C 
            FROM PRODUCT__C 
            WHERE NAME = 'ARCHAN' 
            LIMIT 1
        ];

        IF (!PRODSTODELETE.ISEMPTY()) {
            TRY {
                DELETE PRODSTODELETE;
                SYSTEM.DEBUG('PRODUCT DELETED SUCCESSFULLY.');
            } CATCH (DMLEXCEPTION E) {
                SYSTEM.DEBUG('ERROR DELETING PRODUCT: ' + E.GETMESSAGE());
            }
        } ELSE {
            SYSTEM.DEBUG('NO MATCHING PRODUCT FOUND TO DELETE.');
        }
    }
}

