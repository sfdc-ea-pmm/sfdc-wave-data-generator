package pmmtech;

import java.util.List;
import java.util.Random;

/**
 * RandomLeadProductInterestSelector
 */
public class RandomLeadProductInterestSelector {

    private List<LeadProductInterest> listOfLeadProductInterest;
    private Random rand = new Random();
    private int totalSum = 0;

    public RandomLeadProductInterestSelector(List<LeadProductInterest> lstLeadProdInt){
        this.listOfLeadProductInterest = lstLeadProdInt;
        for(LeadProductInterest acctRT : this.listOfLeadProductInterest) {
            totalSum = totalSum + acctRT.getRelativeProbability();
        }
    }
    
    public LeadProductInterest getRandomLeadProductInterest() {

        int index = rand.nextInt(totalSum) + 1;
        int sum = 0;
        int i = 0;
        
        while(sum < index) {
            sum = sum + this.listOfLeadProductInterest.get(i++).getRelativeProbability();
        }

        return this.listOfLeadProductInterest.get(i-1);
    }
}