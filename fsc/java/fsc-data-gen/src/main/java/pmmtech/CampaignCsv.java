package pmmtech;

import com.opencsv.bean.CsvBindByName;

/**
 * CampaignCsv
 */
public class CampaignCsv {

    @CsvBindByName(column = "Id")
    private String id;
    
    @CsvBindByName(column = "Name")
    private String name;
    
    @CsvBindByName(column = "StartDate")
    private String startDate;

    @CsvBindByName(column = "NumberSent")
    private int numberSent;

    @CsvBindByName(column = "NumberOfResponses")
    private int numberOfResponses;

    @CsvBindByName(column = "NumberOfWonOpportunities")
    private int numberOfWonOpportunities;

    @CsvBindByName(column = "Type")
    private String type;

    @CsvBindByName(column = "OwnerId")
    private String ownerId;

    @CsvBindByName(column = "OwnerName")
    private String ownerName;

    @CsvBindByName(column = "OwnerState")
    private String ownerState;

    @CsvBindByName(column = "OwnerCity")
    private String ownerCity;

    @CsvBindByName(column = "ActualCost")
    private int actualCost;

    @CsvBindByName(column = "IsActive")
    private boolean isActive;

    @CsvBindByName(column = "Status")
    private String status;

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

    public void setOwnerData(UserOwnerCsv ownerData){
        this.setOwnerCity(ownerData.getCity());
        this.setOwnerName(ownerData.getName());
        this.setOwnerState(ownerData.getState());
        this.setOwnerId(ownerData.getId());
    }

    public String getName() {
        return this.name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getNumberOfWonOpportunities() {
        return this.numberOfWonOpportunities;
    }

    public void setNumberOfWonOpportunities(int numberOfWonOpportunities) {
        this.numberOfWonOpportunities = numberOfWonOpportunities;
    }

    public String getType() {
        return this.type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public String getOwnerName() {
        return this.ownerName;
    }

    public void setOwnerName(String ownerName) {
        this.ownerName = ownerName;
    }

    public String getOwnerState() {
        return this.ownerState;
    }

    public void setOwnerState(String ownerState) {
        this.ownerState = ownerState;
    }

    public String getOwnerCity() {
        return this.ownerCity;
    }

    public void setOwnerCity(String ownerCity) {
        this.ownerCity = ownerCity;
    }

    public int getActualCost() {
        return this.actualCost;
    }

    public void setActualCost(int actualCost) {
        this.actualCost = actualCost;
    }

    public String getOwnerId() {
        return this.ownerId;
    }

    public void setOwnerId(String ownerId) {
        this.ownerId = ownerId;
    }

    public boolean getIsActive() {
        return this.isActive;
    }

    public void setIsActive(boolean isAct) {
        this.isActive = isAct;
    }

    public boolean isIsActive() {
        return this.isActive;
    }

    public String getStatus() {
        return this.status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

}