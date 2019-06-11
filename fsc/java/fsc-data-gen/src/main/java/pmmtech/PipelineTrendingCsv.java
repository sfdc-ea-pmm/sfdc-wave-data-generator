package pmmtech;

import com.opencsv.bean.CsvBindByName;

/**
 * PipelineTrendingCsv
 */
public class PipelineTrendingCsv {

    // Opportunity fields

    @CsvBindByName(column = "OpportunityId")
    private String opportunityId;

    @CsvBindByName(column = "CreatedDate")
    private String createdDate;

    @CsvBindByName(column = "OpportunityOwnerId")
    private String opportunityOwnerId;

    @CsvBindByName(column = "OpportunityOwner")
    private String opportunityOwner;    

    @CsvBindByName(column = "OpportunityOwnerState", required = false)
    private String opportunityOwnerState;

    @CsvBindByName(column = "OpportunityOwnerCity", required = false)
    private String opportunityOwnerCity;

    @CsvBindByName(column = "OpportunityAmount")
    private int opportunityAmount;

    @CsvBindByName(column = "OpportunityCloseDate")
    private String opportunityCloseDate;

    @CsvBindByName(column = "OpportunityName")
    private String opportunityName;

    @CsvBindByName(column = "OpportunityForecastCategoryName")
    private String opportunityForecastCategoryName;

    @CsvBindByName(column = "OpportunityAge", required = false)
    private int opportunityAge;

    @CsvBindByName(column = "OpportunityRecordTypeName")
    private String opportunityRecordTypeName;
    
    @CsvBindByName(column = "Type")
    private String opportunityType;

    @CsvBindByName(column = "StageName")
    private String stageName;

    @CsvBindByName(column = "OpportunityIsClosed")
    private boolean opportunityIsClosed;

    @CsvBindByName(column = "OpportunityIsWon")
    private boolean opportunityIsWon;

    // Account fields
    @CsvBindByName(column = "AccountIndustry")
    private String accountIndustry;

    @CsvBindByName(column = "AccountName")
    private String accountName;    

    @CsvBindByName(column = "AccountId", required = false)
    private String accountId;

    @CsvBindByName(column = "AccountClientCategory", required = false)
    private String accountClientCategory;

    @CsvBindByName(column = "AccountMarketingSegment", required = false)
    private String accountMarketingSegment;

    @CsvBindByName(column = "AccountBillingCountry", required = false)
    private String accountBillingCountry;

    // Trending fields

    @CsvBindByName(column = "CloseDate")
    private String closeDate;

    @CsvBindByName(column = "Duration")
    private int duration;

    @CsvBindByName(column = "StageSortOrder")
    private int stageSortOrder;

    @CsvBindByName(column = "PipelineAmount")
    private int pipelineAmount;

    @CsvBindByName(column = "ValidFromDate")
    private String validFromDate;

    @CsvBindByName(column = "ValidToDate")
    private String validToDate;

    @CsvBindByName(column = "StageIsClosed")
    private boolean stageIsClosed;

    @CsvBindByName(column = "StageIsWon")
    private boolean stageIsWon;

    @CsvBindByName(column = "DaysSinceLastActivity", required = false)
    private int daysSinceLastActivity;

    @CsvBindByName(column = "Stage")
    private String stage;
    
    @CsvBindByName(column = "LeadSource")
    private String leadSource;
    
    public void setOpportunityData(OpportunityCsv opptyData){
        this.setAccountBillingCountry("USA");
        this.setAccountClientCategory(opptyData.getAccountClientCategory());
        this.setAccountId(opptyData.getAccountId());
        this.setAccountIndustry(opptyData.getAccountIndustry());
        this.setAccountMarketingSegment(opptyData.getAccountMarketingSegment());
        this.setAccountName(opptyData.getAccountName());
        this.setOpportunityAge(opptyData.getOpportunityAge());
        this.setOpportunityAmount(opptyData.getAmount());
        this.setOpportunityCloseDate(opptyData.getCloseDate());
        this.setOpportunityForecastCategoryName(opptyData.getForecastCategory());
        this.setOpportunityId(opptyData.getId());
        this.setOpportunityIsClosed(opptyData.isClosed());
        this.setOpportunityIsWon(opptyData.isWon());
        this.setOpportunityName(opptyData.getName());
        this.setOpportunityOwner(opptyData.getOpportunityOwner());
        this.setOpportunityOwnerCity(opptyData.getOwnerCity());
        this.setOpportunityOwnerId(opptyData.getOwnerId());
        this.setOpportunityOwnerState(opptyData.getOwnerState());
        this.setDaysSinceLastActivity(opptyData.getDaysSinceLastActivity());

        // Type and RecordTypeName are retrieved from Pipeline Trending source CSV
    }

    public String getOpportunityId() {
        return this.opportunityId;
    }

    public void setOpportunityId(String opportunityId) {
        this.opportunityId = opportunityId;
    }

    public String getCreatedDate() {
        return this.createdDate;
    }

    public void setCreatedDate(String createdDate) {
        this.createdDate = createdDate;
    }

    public String getOpportunityOwnerId() {
        return this.opportunityOwnerId;
    }

    public void setOpportunityOwnerId(String opportunityOwnerId) {
        this.opportunityOwnerId = opportunityOwnerId;
    }

    public String getOpportunityOwner() {
        return this.opportunityOwner;
    }

    public void setOpportunityOwner(String opportunityOwner) {
        this.opportunityOwner = opportunityOwner;
    }

    public String getOpportunityOwnerState() {
        return this.opportunityOwnerState;
    }

    public void setOpportunityOwnerState(String opportunityOwnerState) {
        this.opportunityOwnerState = opportunityOwnerState;
    }

    public String getOpportunityOwnerCity() {
        return this.opportunityOwnerCity;
    }

    public void setOpportunityOwnerCity(String opportunityOwnerCity) {
        this.opportunityOwnerCity = opportunityOwnerCity;
    }

    public int getOpportunityAmount() {
        return this.opportunityAmount;
    }

    public void setOpportunityAmount(int opportunityAmount) {
        this.opportunityAmount = opportunityAmount;
    }

    public String getOpportunityCloseDate() {
        return this.opportunityCloseDate;
    }

    public void setOpportunityCloseDate(String opportunityCloseDate) {
        this.opportunityCloseDate = opportunityCloseDate;
    }

    public String getOpportunityName() {
        return this.opportunityName;
    }

    public void setOpportunityName(String opportunityName) {
        this.opportunityName = opportunityName;
    }

    public String getOpportunityForecastCategoryName() {
        return this.opportunityForecastCategoryName;
    }

    public void setOpportunityForecastCategoryName(String opportunityForecastCategoryName) {
        this.opportunityForecastCategoryName = opportunityForecastCategoryName;
    }

    public int getOpportunityAge() {
        return this.opportunityAge;
    }

    public void setOpportunityAge(int opportunityAge) {
        this.opportunityAge = opportunityAge;
    }

    public String getOpportunityRecordTypeName() {
        return this.opportunityRecordTypeName;
    }

    public void setOpportunityRecordTypeName(String opportunityRecordTypeName) {
        this.opportunityRecordTypeName = opportunityRecordTypeName;
    }

    public String getOpportunityType() {
        return this.opportunityType;
    }

    public void setOpportunityType(String opportunityType) {
        this.opportunityType = opportunityType;
    }

    public String getStageName() {
        return this.stageName;
    }

    public void setStageName(String stageName) {
        this.stageName = stageName;
    }

    public boolean isOpportunityIsClosed() {
        return this.opportunityIsClosed;
    }

    public boolean getOpportunityIsClosed() {
        return this.opportunityIsClosed;
    }

    public void setOpportunityIsClosed(boolean opportunityIsClosed) {
        this.opportunityIsClosed = opportunityIsClosed;
    }

    public boolean isOpportunityIsWon() {
        return this.opportunityIsWon;
    }

    public boolean getOpportunityIsWon() {
        return this.opportunityIsWon;
    }

    public void setOpportunityIsWon(boolean opportunityIsWon) {
        this.opportunityIsWon = opportunityIsWon;
    }

    public String getAccountIndustry() {
        return this.accountIndustry;
    }

    public void setAccountIndustry(String accountIndustry) {
        this.accountIndustry = accountIndustry;
    }

    public String getAccountName() {
        return this.accountName;
    }

    public void setAccountName(String accountName) {
        this.accountName = accountName;
    }

    public String getAccountId() {
        return this.accountId;
    }

    public void setAccountId(String accountId) {
        this.accountId = accountId;
    }

    public String getAccountClientCategory() {
        return this.accountClientCategory;
    }

    public void setAccountClientCategory(String accountClientCategory) {
        this.accountClientCategory = accountClientCategory;
    }

    public String getAccountMarketingSegment() {
        return this.accountMarketingSegment;
    }

    public void setAccountMarketingSegment(String accountMarketingSegment) {
        this.accountMarketingSegment = accountMarketingSegment;
    }

    public String getCloseDate() {
        return this.closeDate;
    }

    public void setCloseDate(String closeDate) {
        this.closeDate = closeDate;
    }

    public int getDuration() {
        return this.duration;
    }

    public void setDuration(int duration) {
        this.duration = duration;
    }

    public int getStageSortOrder() {
        return this.stageSortOrder;
    }

    public void setStageSortOrder(int stageSortOrder) {
        this.stageSortOrder = stageSortOrder;
    }

    public int getPipelineAmount() {
        return this.pipelineAmount;
    }

    public void setPipelineAmount(int pipelineAmount) {
        this.pipelineAmount = pipelineAmount;
    }

    public String getValidFromDate() {
        return this.validFromDate;
    }

    public void setValidFromDate(String validFromDate) {
        this.validFromDate = validFromDate;
    }

    public String getValidToDate() {
        return this.validToDate;
    }

    public void setValidToDate(String validToDate) {
        this.validToDate = validToDate;
    }

    public boolean isStageIsClosed() {
        return this.stageIsClosed;
    }

    public boolean getStageIsClosed() {
        return this.stageIsClosed;
    }

    public void setStageIsClosed(boolean stageIsClosed) {
        this.stageIsClosed = stageIsClosed;
    }

    public boolean isStageIsWon() {
        return this.stageIsWon;
    }

    public boolean getStageIsWon() {
        return this.stageIsWon;
    }

    public void setStageIsWon(boolean stageIsWon) {
        this.stageIsWon = stageIsWon;
    }

    public int getDaysSinceLastActivity() {
        return this.daysSinceLastActivity;
    }

    public void setDaysSinceLastActivity(int daysSinceLastActivity) {
        this.daysSinceLastActivity = daysSinceLastActivity;
    }

    public String getStage() {
        return this.stage;
    }

    public void setStage(String stage) {
        this.stage = stage;
    }

    public String getLeadSource() {
        return this.leadSource;
    }

    public void setLeadSource(String leadSource) {
        this.leadSource = leadSource;
    }

    public String getAccountBillingCountry() {
        return this.accountBillingCountry;
    }

    public void setAccountBillingCountry(String accountBillingCountry) {
        this.accountBillingCountry = accountBillingCountry;
    }

}