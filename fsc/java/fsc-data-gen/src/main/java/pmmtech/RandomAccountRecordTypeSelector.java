package pmmtech;

import java.util.List;
import java.util.Random;

/**
 * RandomAccountRecordTypeSelector
 * https://stackoverflow.com/questions/9330394/how-to-pick-an-item-by-its-probability
 */
public class RandomAccountRecordTypeSelector {

    private List<AccountRecordType> listOfAccountsRecordTypes;
    private Random rand = new Random();
    private int totalSum = 0;

    public RandomAccountRecordTypeSelector(List<AccountRecordType> lstAccounts){
        this.listOfAccountsRecordTypes = lstAccounts;
        for(AccountRecordType acctRT : this.listOfAccountsRecordTypes) {
            totalSum = totalSum + acctRT.getRelativeProbability();
        }
    }
    
    public AccountRecordType getRandomAccountRecordType() {

        int index = rand.nextInt(totalSum) + 1;
        int sum = 0;
        int i = 0;
        
        while(sum < index) {
            sum = sum + this.listOfAccountsRecordTypes.get(i++).getRelativeProbability();
        }

        return this.listOfAccountsRecordTypes.get(i-1);
    }
}