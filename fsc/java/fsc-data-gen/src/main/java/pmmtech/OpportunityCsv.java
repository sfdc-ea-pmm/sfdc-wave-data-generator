package pmmtech;

import com.opencsv.bean.CsvBindByName;

/**
 * OpportunityCsv
 */
public class OpportunityCsv {

    @CsvBindByName(column = "Id")
    private String id;

    @CsvBindByName(column = "OpportunityName")
    private String name;

    @CsvBindByName(column = "AccountIndustry")
    private String accountIndustry;

    @CsvBindByName(column = "AccountName")
    private String accountName;

    @CsvBindByName(column = "AccountId")
    private String accountId;

    @CsvBindByName(column = "AccountClientCategory", required = false)
    private String accountClientCategory;

    @CsvBindByName(column = "AccountMarketingSegment", required = false)
    private String accountMarketingSegment;

    @CsvBindByName(column = "Amount")
    private int amount;

    @CsvBindByName(column = "ExpectedRevenue", required = false)
    private int expectedRevenue;

    @CsvBindByName(column = "CloseDate")
    private String closeDate;

    @CsvBindByName(column = "DaysSinceLastActivity")
    private int daysSinceLastActivity;

    @CsvBindByName(column = "ForecastCategory")
    private String forecastCategory;

    @CsvBindByName(column = "IsClosed")
    private boolean closed;

    @CsvBindByName(column = "IsWon")
    private boolean won;

    @CsvBindByName(column = "OpportunityAge")
    private int opportunityAge;

    @CsvBindByName(column = "OpportunityOwner")
    private String opportunityOwner;

    @CsvBindByName(column = "OwnerId")
    private String ownerId;

    @CsvBindByName(column = "OwnerState", required = false)
    private String ownerState;

    @CsvBindByName(column = "OwnerCity", required = false)
    private String ownerCity;

    @CsvBindByName(column = "OwnerSmallPhotoUrl", required = false)
    private String ownerSmallPhotoUrl;

    @CsvBindByName(column = "StageName")
    private String stageName;

    @CsvBindByName(column = "Stage")
    private String stage;

    @CsvBindByName(column = "LeadSource")
    private String leadSource;

    @CsvBindByName(column = "StageSortOrder")
    private int stageSortOrder;

    @CsvBindByName(column = "TimeInStageDurationSeconds")
    private long timeInStageDurationSeconds;

    @CsvBindByName(column = "Probability")
    private int probability;

    @CsvBindByName(column = "ActivityId", required = false)
    private String activityId;

    @CsvBindByName(column = "RecordTypeName", required = false)
    private String recordTypeName;

    public void setAccountData(AccountCsv accData){
        this.setAccountId(accData.getId());
        this.setAccountIndustry(accData.getIndustry());
        this.setAccountName(accData.getName());
        this.setAccountClientCategory(accData.getClientCategory());
        this.setAccountMarketingSegment(accData.getMarketingSegment());
    }

    public void setOwnerData(UserOwnerCsv ownerData){
        this.setOwnerId(ownerData.getId());
        this.setOpportunityOwner(ownerData.getName());
        this.setOwnerCity(ownerData.getCity());
        this.setOwnerSmallPhotoUrl(ownerData.getSmallPhotoUrl());
        this.setOwnerState(ownerData.getState());
    }

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

    public int getAmount() {
        return this.amount;
    }

    public void setAmount(int amount) {
        this.amount = amount;
    }

    public String getCloseDate() {
        return this.closeDate;
    }

    public void setCloseDate(String closeDate) {
        this.closeDate = closeDate;
    }

    public int getDaysSinceLastActivity() {
        return this.daysSinceLastActivity;
    }

    public void setDaysSinceLastActivity(int daysSinceLastActivity) {
        this.daysSinceLastActivity = daysSinceLastActivity;
    }

    public String getForecastCategory() {
        return this.forecastCategory;
    }

    public void setForecastCategory(String forecastCategory) {
        this.forecastCategory = forecastCategory;
    }

    public boolean isClosed() {
        return this.closed;
    }

    public boolean getClosed() {
        return this.closed;
    }

    public void setClosed(boolean closed) {
        this.closed = closed;
    }

    public boolean isWon() {
        return this.won;
    }

    public boolean getWon() {
        return this.won;
    }

    public void setWon(boolean won) {
        this.won = won;
    }

    public int getOpportunityAge() {
        return this.opportunityAge;
    }

    public void setOpportunityAge(int opportunityAge) {
        this.opportunityAge = opportunityAge;
    }

    public String getOpportunityOwner() {
        return this.opportunityOwner;
    }

    public void setOpportunityOwner(String opportunityOwner) {
        this.opportunityOwner = opportunityOwner;
    }

    public String getOwnerId() {
        return this.ownerId;
    }

    public void setOwnerId(String ownerId) {
        this.ownerId = ownerId;
    }

    public String getStageName() {
        return this.stageName;
    }

    public void setStageName(String stageName) {
        this.stageName = stageName;
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

    public int getStageSortOrder() {
        return this.stageSortOrder;
    }

    public void setStageSortOrder(int stageSortOrder) {
        this.stageSortOrder = stageSortOrder;
    }

    public long getTimeInStageDurationSeconds() {
        return this.timeInStageDurationSeconds;
    }

    public void setTimeInStageDurationSeconds(long timeInStageDurationSeconds) {
        this.timeInStageDurationSeconds = timeInStageDurationSeconds;
    }

    public int getProbability() {
        return this.probability;
    }

    public void setProbability(int probability) {
        this.probability = probability;
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

    public String getActivityId() {
        return this.activityId;
    }

    public void setActivityId(String activityId) {
        this.activityId = activityId;
    }

    public int getExpectedRevenue() {
        return this.expectedRevenue <= 0 ? this.amount : this.expectedRevenue;
    }

    public void setExpectedRevenue(int expectedRevenue) {
        this.expectedRevenue = expectedRevenue;
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

    public String getOwnerSmallPhotoUrl() {
        return this.ownerSmallPhotoUrl;
    }

    public void setOwnerSmallPhotoUrl(String ownerSmallPhotoUrl) {
        this.ownerSmallPhotoUrl = ownerSmallPhotoUrl;
    }

    public String getRecordTypeName() {
        return this.recordTypeName;
    }

    public void setRecordTypeName(String recordTypeName) {
        this.recordTypeName = recordTypeName;
    }

}