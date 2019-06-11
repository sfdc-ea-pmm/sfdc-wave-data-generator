package pmmtech;

import java.util.List;
import java.util.Random;

/**
 * RandomBillingStateSelector
 */
public class RandomBillingStateSelector {

    private List<BillingState> listOfBillingStates;
    private Random rand = new Random();
    private int totalSum = 0;

    public RandomBillingStateSelector(List<BillingState> lstBs){
        this.listOfBillingStates = lstBs;
        for(BillingState billingState : this.listOfBillingStates) {
            totalSum = totalSum + billingState.getRelativeProbability();
        }
    }
    
    public BillingState getRandomBillingState() {

        int index = rand.nextInt(totalSum) + 1;
        int sum = 0;
        int i = 0;
        
        while(sum < index) {
            sum = sum + this.listOfBillingStates.get(i++).getRelativeProbability();
        }

        return this.listOfBillingStates.get(i-1);
    }
}