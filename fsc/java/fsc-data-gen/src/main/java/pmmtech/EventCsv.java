package pmmtech;

import com.opencsv.bean.CsvBindByName;

/**
 * EventCsv
 */
public class EventCsv {

    @CsvBindByName(column = "LeadId")
    private String leadId;

    @CsvBindByName(column = "ActivityDate")
    private String activityDate;

    @CsvBindByName(column = "LeadCreatedDate")
    private String leadCreatedDate;

    @CsvBindByName(column = "LeadOwnerId")
    private String leadOwnerId;
    
    @CsvBindByName(column = "LeadOwnerName")
    private String leadOwnerName;

    @CsvBindByName(column = "LeadOwnerState", required = false)
    private String leadOwnerState;

    @CsvBindByName(column = "LeadOwnerCity", required = false)
    private String leadOwnerCity;

    @CsvBindByName(column = "Touches")
    private int touches;

    @CsvBindByName(column = "OwnerId")
    private String ownerId;

    @CsvBindByName(column = "OwnerName", required = false)
    private String ownerName;

    @CsvBindByName(column = "OwnerState", required = false)
    private String ownerState;

    @CsvBindByName(column = "OwnerCity", required = false)
    private String ownerCity;

    public String getLeadId() {
        return this.leadId;
    }

    public void setLeadId(String leadId) {
        this.leadId = leadId;
    }

    public String getActivityDate() {
        return this.activityDate;
    }

    public void setActivityDate(String activityDate) {
        this.activityDate = activityDate;
    }

    public String getLeadOwnerName() {
        return this.leadOwnerName;
    }

    public void setLeadOwnerName(String leadOwnerName) {
        this.leadOwnerName = leadOwnerName;
    }

    public int getTouches() {
        return this.touches;
    }

    public void setTouches(int touches) {
        this.touches = touches;
    }

    public String getOwnerId() {
        return this.ownerId;
    }

    public void setOwnerId(String ownerId) {
        this.ownerId = ownerId;
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

    public void setOwnerData(UserOwnerCsv ownerData){
        this.setOwnerCity(ownerData.getCity());
        this.setOwnerId(ownerData.getId());
        this.setOwnerName(ownerData.getName());
        this.setOwnerState(ownerData.getState());
    }

    public void setLeadData(LeadCsv leadData){
        this.setLeadOwnerCity(leadData.getOwnerCity());
        this.setLeadId(leadData.getId());
        this.setLeadOwnerId(leadData.getOwnerId());
        this.setLeadOwnerName(leadData.getOwnerName());
        this.setLeadOwnerState(leadData.getOwnerState());
        this.setLeadCreatedDate(leadData.getCreatedDate());
    }

    public String getLeadCreatedDate() {
        return this.leadCreatedDate;
    }

    public void setLeadCreatedDate(String leadCreatedDate) {
        this.leadCreatedDate = leadCreatedDate;
    }

    public String getLeadOwnerState() {
        return this.leadOwnerState;
    }

    public void setLeadOwnerState(String leadOwnerState) {
        this.leadOwnerState = leadOwnerState;
    }

    public String getLeadOwnerCity() {
        return this.leadOwnerCity;
    }

    public void setLeadOwnerCity(String leadOwnerCity) {
        this.leadOwnerCity = leadOwnerCity;
    }

    public String getLeadOwnerId() {
        return this.leadOwnerId;
    }

    public void setLeadOwnerId(String leadOwnerId) {
        this.leadOwnerId = leadOwnerId;
    }

}