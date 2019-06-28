package pmmtech;

import com.opencsv.bean.CsvBindByName;

/**
 * CampaignMemberCsv
 */
public class CampaignMemberCsv {

    @CsvBindByName(column = "Id")
    private String id;
    
    @CsvBindByName(column = "Name")
    private String name;

    @CsvBindByName(column = "HasResponded")
    private boolean hasResponded;

    @CsvBindByName(column = "Type")
    private String type;

    @CsvBindByName(column = "CampaignId")
    private String campaignId;

    @CsvBindByName(column = "campaignName")
    private String campaignName;

    @CsvBindByName(column = "CampaignType")
    private String campaignType;

    @CsvBindByName(column = "CampaignStartDate")
    private String campaignStartDate;

    @CsvBindByName(column = "CampaignIsActive")
    private boolean campaignIsActive;

    @CsvBindByName(column = "CampaignStatus")
    private String campaignStatus;

    @CsvBindByName(column = "ContactEmail")
    private String contactEmail;

    @CsvBindByName(column = "ContactName")
    private String contactName;

    @CsvBindByName(column = "ContactMobilePhone")
    private String contactMobilePhone;

    @CsvBindByName(column = "LeadEmail")
    private String leadEmail;

    @CsvBindByName(column = "LeadName")
    private String leadName;

    @CsvBindByName(column = "LeadPhone")
    private String leadPhone;

    public String getId() {
        return this.id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getName() {
        return this.name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getType() {
        return this.type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public String getCampaignStartDate() {
        return this.campaignStartDate;
    }

    public void setCampaignStartDate(String stDate) {
        this.campaignStartDate = stDate;
    }

    public String getCampaignId() {
        return this.campaignId;
    }

    public void setCampaignId(String campaignId) {
        this.campaignId = campaignId;
    }

    public boolean getHasResponded() {
        return this.hasResponded;
    }

    public void setHasResponded(boolean hasResponded) {
        this.hasResponded = hasResponded;
    }

    public void setCampaignData(CampaignCsv campData){
        this.setCampaignName(campData.getName());
        this.setCampaignType(campData.getType());
        this.setCampaignStartDate(campData.getStartDate());
        this.setCampaignIsActive(campData.getIsActive());
        this.setCampaignStatus(campData.getStatus());
    }

    private void setCampaignType(String campaignType) {
        this.campaignType = campaignType;
    }
    public String getCampaignType() {
        return this.campaignType;
    }
    private void setCampaignName(String campaignName) {
        this.campaignName = campaignName;
    }
    public String getCampaignName() {
        return this.campaignName;
    }

    private void setCampaignIsActive(boolean campaignIsActive) {
        this.campaignIsActive = campaignIsActive;
    }
    public boolean getCampaignIsActive() {
        return this.campaignIsActive;
    }

    public boolean isHasResponded() {
        return this.hasResponded;
    }

    public boolean isCampaignIsActive() {
        return this.campaignIsActive;
    }

    public String getCampaignStatus() {
        return this.campaignStatus;
    }

    public void setCampaignStatus(String campaignStatus) {
        this.campaignStatus = campaignStatus;
    }

    public String getContactEmail() {
        return this.contactEmail;
    }

    public void setContactEmail(String contactEmail) {
        this.contactEmail = contactEmail;
    }

    public String getContactName() {
        return this.contactName;
    }

    public void setContactName(String contactName) {
        this.contactName = contactName;
    }

    public String getContactMobilePhone() {
        return this.contactMobilePhone;
    }

    public void setContactMobilePhone(String contactMobilePhone) {
        this.contactMobilePhone = contactMobilePhone;
    }

    public String getLeadEmail() {
        return this.leadEmail;
    }

    public void setLeadEmail(String leadEmail) {
        this.leadEmail = leadEmail;
    }

    public String getLeadName() {
        return this.leadName;
    }

    public void setLeadName(String leadName) {
        this.leadName = leadName;
    }

    public String getLeadPhone() {
        return this.leadPhone;
    }

    public void setLeadPhone(String leadPhone) {
        this.leadPhone = leadPhone;
    }

}