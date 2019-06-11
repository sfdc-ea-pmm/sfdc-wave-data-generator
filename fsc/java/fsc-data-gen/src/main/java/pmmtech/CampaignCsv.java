package pmmtech;

import com.opencsv.bean.CsvBindByName;

/**
 * CampaignCsv
 */
public class CampaignCsv {

    @CsvBindByName(column = "Id")
    private String id;
    
    @CsvBindByName(column = "StartDate")
    private String startDate;

    @CsvBindByName(column = "NumberSent")
    private int numberSent;

    @CsvBindByName(column = "NumberOfResponses")
    private int numberOfResponses;

    public String getId() {
        return this.id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getStartDate() {
        return this.startDate;
    }

    public void setStartDate(String stDate) {
        this.startDate = stDate;
    }

    public int getNumberSent() {
        return this.numberSent;
    }

    public void setNumberSent(int numberSent) {
        this.numberSent = numberSent;
    }

    public int getNumberOfResponses() {
        return this.numberOfResponses;
    }

    public void setNumberOfResponses(int numberOfResponses) {
        this.numberOfResponses = numberOfResponses;
    }

}