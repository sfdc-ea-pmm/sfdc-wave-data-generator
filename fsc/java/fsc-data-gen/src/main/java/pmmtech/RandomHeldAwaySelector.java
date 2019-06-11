package pmmtech;

import java.util.List;
import java.util.Random;

/**
 * RandomHeldAwaySelector
 */
public class RandomHeldAwaySelector {

    private List<HeldAwayItem> listOfHeldAwayItems;
    private Random rand = new Random();
    private int totalSum = 0;

    public RandomHeldAwaySelector(List<HeldAwayItem> lstHA){
        this.listOfHeldAwayItems = lstHA;
        for(HeldAwayItem haItem : this.listOfHeldAwayItems) {
            totalSum = totalSum + haItem.getRelativeProbability();
        }
    }
    
    public HeldAwayItem getRandomHeldAwayItem() {

        int index = rand.nextInt(totalSum) + 1;
        int sum = 0;
        int i = 0;
        
        while(sum < index) {
            sum = sum + this.listOfHeldAwayItems.get(i++).getRelativeProbability();
        }

        return this.listOfHeldAwayItems.get(i-1);
    }
}