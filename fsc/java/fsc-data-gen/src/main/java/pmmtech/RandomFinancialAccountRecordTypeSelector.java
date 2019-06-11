package pmmtech;

import java.util.List;
import java.util.Random;

/**
 * RandomFinancialAccountRecordTypeSelector
 */
public class RandomFinancialAccountRecordTypeSelector {

    private List<FinancialAccountRecordType> listOfFinAccountsRecordTypes;
    private Random rand = new Random();
    private int totalSum = 0;

    public RandomFinancialAccountRecordTypeSelector(List<FinancialAccountRecordType> lstFinAccRTs){
        this.listOfFinAccountsRecordTypes = lstFinAccRTs;
        for(FinancialAccountRecordType finAcctRT : this.listOfFinAccountsRecordTypes) {
            totalSum = totalSum + finAcctRT.getRelativeProbability();
        }
    }
    
    public FinancialAccountRecordType getRandomFinancialAccountRecordType() {

        int index = rand.nextInt(totalSum) + 1;
        int sum = 0;
        int i = 0;
        
        while(sum < index) {
            sum = sum + this.listOfFinAccountsRecordTypes.get(i++).getRelativeProbability();
        }

        return this.listOfFinAccountsRecordTypes.get(i-1);
    }
}