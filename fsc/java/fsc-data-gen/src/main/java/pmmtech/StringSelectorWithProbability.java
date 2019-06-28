package pmmtech;

import java.util.List;
import java.util.Random;

/**
 * StringSelectorWithProbability
 */
public class StringSelectorWithProbability {

    private List<RandomString> listOfStrings;
    private Random rand = new Random();
    private int totalSum = 0;

    public StringSelectorWithProbability(List<RandomString> lstRandomStrings){
        this.listOfStrings = lstRandomStrings;
        for(RandomString s : this.listOfStrings) {
            totalSum = totalSum + s.getRelativeProbability();
        }
    }

    public RandomString getRandomString() {

        int index = rand.nextInt(totalSum) + 1;
        int sum = 0;
        int i = 0;
        
        while(sum < index) {
            sum = sum + this.listOfStrings.get(i++).getRelativeProbability();
        }

        return this.listOfStrings.get(i-1);
    }
}