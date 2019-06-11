package pmmtech;

import java.util.HashMap;
import java.util.LinkedList;
import java.util.Map;

/**
 * Unit test for simple App.
 */
public class AppTest 
{
    public void testRandomAccountRecordTypeSelector(){
        LinkedList<AccountRecordType> lstRecordTypes = new LinkedList<AccountRecordType>();
            
        // Account Record Type based on probability
        AccountRecordType aRt;
        
        // Individual Record Type
        aRt = new AccountRecordType();
        aRt.setRelativeProbability(1);
        aRt.setRecordTypeName("Individual");
        lstRecordTypes.add(aRt);

        // Household Record Type
        aRt = new AccountRecordType();
        aRt.setRelativeProbability(1);
        aRt.setRecordTypeName("Household");
        lstRecordTypes.add(aRt);

        // Person Account Record Type
        aRt = new AccountRecordType();
        aRt.setRelativeProbability(2);
        aRt.setRecordTypeName("Person Account");
        lstRecordTypes.add(aRt);

        RandomAccountRecordTypeSelector rndAcctRecTypeSel = new RandomAccountRecordTypeSelector(lstRecordTypes);
        
        Map<String, Integer> rtCounter = new HashMap<String, Integer>();
        rtCounter.put("Household", 0);
        rtCounter.put("Individual", 0);
        rtCounter.put("Person Account", 0);

        for (int i = 1; i <= 100; i++) {
            String rtName = rndAcctRecTypeSel.getRandomAccountRecordType().getRecordTypeName();
            Integer iCounter = rtCounter.get(rtName);
            iCounter++;
            rtCounter.put(rtName, iCounter);
        }

        for (String keyVar : rtCounter.keySet()) {
            System.out.println("Total " + keyVar + ": " + rtCounter.get(keyVar));
        }
    }
}
