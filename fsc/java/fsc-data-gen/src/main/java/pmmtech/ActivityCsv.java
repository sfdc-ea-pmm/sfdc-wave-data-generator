package pmmtech;

import com.opencsv.bean.CsvBindByName;

/**
 * ActivityCsv
 */
public class ActivityCsv {

    @CsvBindByName(column = "Id")
    private String id;

    @CsvBindByName(column = "AccountId")
    private String accountId;

    @CsvBindByName(column = "AccountName")
    private String accountName;

    @CsvBindByName(column = "AccountRecordTypeName")
    private String accountRecordTypeName;

    @CsvBindByName(column = "ActivityDate")
    private String activityDate;

    @CsvBindByName(column = "CreatedDate")
    private String createdDate;

    @CsvBindByName(column = "Type")
    private String type;

    @CsvBindByName(column = "AccountType")
    private String accountType;

    @CsvBindByName(column = "AccountServiceModel")
    private String accountServiceModel;

    @CsvBindByName(column = "AccountOwnerName")
    private String accountOwnerName;

    @CsvBindByName(column = "AccountMarketingSegment")
    private String accountMarketingSegment;

    @CsvBindByName(column = "AccountInvestmentExperience")
    private String accountInvestmentExperience;

    @CsvBindByName(column = "AccountInvestmentObjectives")
    private String accountInvestmentObjectives;

    @CsvBindByName(column = "AccountAUM", required = false)
    private double accountAum;

    @CsvBindByName(column = "Status")
    private String status;

    @CsvBindByName(column = "TaskSubtype")
    private String taskSubtype;

    @CsvBindByName(column = "EventSubtype")
    private String eventSubtype;

    @CsvBindByName(column = "Subject")
    private String subject;

    @CsvBindByName(column = "Priority")
    private String priority;

    @CsvBindByName(column = "Regarding")
    private String regarding;

    @CsvBindByName(column = "RecordTypeName")
    private String recordTypeName;

    @CsvBindByName(column = "OwnerId", required = false)
    private String ownerId;

    @CsvBindByName(column = "OwnerName", required = false)
    private String ownerName;

    @CsvBindByName(column = "OwnerState", required = false)
    private String ownerState;

    @CsvBindByName(column = "OwnerCity", required = false)
    private String ownerCity;

    @CsvBindByName(column = "OwnerRoleName", required = false)
    private String ownerRoleName;

    @CsvBindByName(column = "OwnerEmail", required = false)
    private String ownerEmail;

    @CsvBindByName(column = "OwnerSmallPhotoUrl", required = false)
    private String ownerSmallPhotoUrl;

    public void setAccountData(AccountCsv accData){
        this.accountId = accData.getId();
        this.accountName = accData.getName();
        this.accountRecordTypeName = accData.getRecordTypeName();
        this.accountServiceModel = accData.getServiceModel();
        this.accountOwnerName = accData.getOwnerName();
        this.accountMarketingSegment = accData.getMarketingSegment();
        this.accountInvestmentExperience = accData.getInvestmentExperience();
        this.accountInvestmentObjectives = accData.getInvestmentObjectives();
        this.accountAum = accData.getAum();
    }

    public String getId() {
        return this.id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getAccountId() {
        return this.accountId;
    }

    public void setAccountId(String accountId) {
        this.accountId = accountId;
    }

    public String getAccountName() {
        return this.accountName;
    }

    public void setAccountName(String accountName) {
        this.accountName = accountName;
    }

    public String getAccountRecordTypeName() {
        return this.accountRecordTypeName;
    }

    public void setAccountRecordTypeName(String accountRecordTypeName) {
        this.accountRecordTypeName = accountRecordTypeName;
    }

    public String getActivityDate() {
        return this.activityDate;
    }

    public void setActivityDate(String activityDate) {
        this.activityDate = activityDate;
    }

    public String getType() {
        return this.type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public String getAccountServiceModel() {
        return this.accountServiceModel;
    }

    public void setAccountServiceModel(String accountServiceModel) {
        this.accountServiceModel = accountServiceModel;
    }

    public String getAccountOwnerName() {
        return this.accountOwnerName;
    }

    public void setAccountOwnerName(String accountOwnerName) {
        this.accountOwnerName = accountOwnerName;
    }

    public String getAccountMarketingSegment() {
        return this.accountMarketingSegment;
    }

    public void setAccountMarketingSegment(String accountMarketingSegment) {
        this.accountMarketingSegment = accountMarketingSegment;
    }

    public String getAccountInvestmentExperience() {
        return this.accountInvestmentExperience;
    }

    public void setAccountInvestmentExperience(String accountInvestmentExperience) {
        this.accountInvestmentExperience = accountInvestmentExperience;
    }

    public String getAccountInvestmentObjectives() {
        return this.accountInvestmentObjectives;
    }

    public void setAccountInvestmentObjectives(String accountInvestmentObjectives) {
        this.accountInvestmentObjectives = accountInvestmentObjectives;
    }

    public String getCreatedDate() {
        return this.createdDate;
    }

    public void setCreatedDate(String createdDate) {
        this.createdDate = createdDate;
    }

    public String getAccountType() {
        return this.accountType;
    }

    public void setAccountType(String accountType) {
        this.accountType = accountType;
    }

    public String getStatus() {
        return this.status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public String getTaskSubtype() {
        return this.taskSubtype;
    }

    public void setTaskSubtype(String taskSubtype) {
        this.taskSubtype = taskSubtype;
    }

    public String getEventSubtype() {
        return this.eventSubtype;
    }

    public void setEventSubtype(String eventSubtype) {
        this.eventSubtype = eventSubtype;
    }

    public String getSubject() {
        return this.subject;
    }

    public void setSubject(String subject) {
        this.subject = subject;
    }

    public String getPriority() {
        return this.priority;
    }

    public void setPriority(String priority) {
        this.priority = priority;
    }

    public String getRegarding() {
        return this.regarding;
    }

    public void setRegarding(String regarding) {
        this.regarding = regarding;
    }

    public String getRecordTypeName() {
        return this.recordTypeName;
    }

    public void setRecordTypeName(String recordTypeName) {
        this.recordTypeName = recordTypeName;
    }

    public double getAccountAum() {
        return this.accountAum;
    }

    public void setAccountAum(double accountAum) {
        this.accountAum = accountAum;
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

    public String getOwnerRoleName() {
        return this.ownerRoleName;
    }

    public void setOwnerRoleName(String ownerRoleName) {
        this.ownerRoleName = ownerRoleName;
    }

    public String getOwnerEmail() {
        return this.ownerEmail;
    }

    public void setOwnerEmail(String ownerEmail) {
        this.ownerEmail = ownerEmail;
    }

    public String getOwnerSmallPhotoUrl() {
        return this.ownerSmallPhotoUrl;
    }

    public void setOwnerSmallPhotoUrl(String ownerSmallPhotoUrl) {
        this.ownerSmallPhotoUrl = ownerSmallPhotoUrl;
    }
    
    public void setOwnerData(UserOwnerCsv ownerData){
        this.setOwnerCity(ownerData.getCity());
        this.setOwnerEmail(ownerData.getEmail());
        this.setOwnerId(ownerData.getId());
        this.setOwnerName(ownerData.getName());
        this.setOwnerRoleName(ownerData.getRoleName());
        this.setOwnerSmallPhotoUrl(ownerData.getSmallPhotoUrl());
        this.setOwnerState(ownerData.getState());
    }
}