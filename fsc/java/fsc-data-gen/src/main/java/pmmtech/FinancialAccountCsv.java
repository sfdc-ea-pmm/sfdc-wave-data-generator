package pmmtech;

import java.util.ArrayList;

import com.opencsv.bean.CsvBindByName;

/**
 * FinancialAccoun
 */
public class FinancialAccountCsv {

    @CsvBindByName(column = "Id")
    private String id;

    @CsvBindByName(column = "AccountId")
    private String accountId;

    @CsvBindByName(column = "AccountName")
    private String accountName;

    @CsvBindByName(column = "AccountMarketingSegment")
    private String accountMarketingSegment;

    @CsvBindByName(column = "AccountInvestmentObjectives")
    private String accountInvestmentObjectives;

    @CsvBindByName(column = "AccountServiceModel")
    private String accountServiceModel;

    @CsvBindByName(column = "AccountTotalAUMPrimaryOwner", required = false)
    private double accountTotalAUMPrimaryOwner;

    @CsvBindByName(column = "AccountTotalFinAcctsPrimaryOwner", required = false)
    private double accountTotalFinAcctsPrimaryOwner;

    @CsvBindByName(column = "AccountTotalHeldFinAcctsPrimaryOwner", required = false)
    private double accountTotalHeldFinAcctsPrimaryOwner;

    @CsvBindByName(column = "OwnerId")
    private String ownerId;

    @CsvBindByName(column = "OwnerName")
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

    @CsvBindByName(column = "FinancialAccountType")
    private String financialAccountType;

    @CsvBindByName(column = "JointOwnerId")
    private String jointOwnerId;

    @CsvBindByName(column = "Balance")
    private double balance;

    @CsvBindByName(column = "HeldAway")
    private boolean heldAway;

    @CsvBindByName(column = "Managed")
    private boolean managed;

    @CsvBindByName(column = "RecordTypeName")
    private String recordTypeName;

    @CsvBindByName(column = "Ownership")
    private String ownership;

    @CsvBindByName(column = "CreatedDate")
    private String createdDate;

    private ArrayList<FinancialAccountTransactionCsv> transactions = new ArrayList<FinancialAccountTransactionCsv>();

    public void setAccountData(AccountCsv accountData){
        this.setAccountId(accountData.getId());
        this.setAccountInvestmentObjectives(accountData.getInvestmentObjectives());
        this.setAccountMarketingSegment(accountData.getMarketingSegment());
        this.setAccountName(accountData.getName());
        this.setAccountServiceModel(accountData.getServiceModel());
        this.setAccountTotalAUMPrimaryOwner(accountData.getTotalAUMPrimaryOwner());
        this.setAccountTotalFinAcctsPrimaryOwner(accountData.getTotalFinAcctsPrimaryOwner());
        this.setAccountTotalHeldFinAcctsPrimaryOwner(accountData.getTotalHeldFinAcctsPrimaryOwner());
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

    public String getAccountMarketingSegment() {
        return this.accountMarketingSegment;
    }

    public void setAccountMarketingSegment(String accountMarketingSegment) {
        this.accountMarketingSegment = accountMarketingSegment;
    }

    public String getAccountInvestmentObjectives() {
        return this.accountInvestmentObjectives;
    }

    public void setAccountInvestmentObjectives(String accountInvestmentObjectives) {
        this.accountInvestmentObjectives = accountInvestmentObjectives;
    }

    public String getAccountServiceModel() {
        return this.accountServiceModel;
    }

    public void setAccountServiceModel(String accountServiceModel) {
        this.accountServiceModel = accountServiceModel;
    }

    public String getOwnerName() {
        return this.ownerName;
    }

    public void setOwnerName(String ownerName) {
        this.ownerName = ownerName;
    }

    public String getFinancialAccountType() {
        return this.financialAccountType;
    }

    public void setFinancialAccountType(String financialAccountType) {
        this.financialAccountType = financialAccountType;
    }

    public String getJointOwnerId() {
        return this.jointOwnerId;
    }

    public void setJoinOwnerId(String jointOwnerId) {
        this.jointOwnerId = jointOwnerId;
    }

    public double getBalance() {
        return this.balance;
    }

    public void setBalance(double balance) {
        this.balance = balance;
    }
	public void setJointOwnerId(String jointOwnerId) {
        this.jointOwnerId = jointOwnerId;
    }

    public boolean isHeldAway() {
        return this.heldAway;
    }

    public boolean getHeldAway() {
        return this.heldAway;
    }

    public void setHeldAway(boolean heldAway) {
        this.heldAway = heldAway;
    }

    public static String[] getCsvHeader(){
        String[] headerRecord = {
            "Id",
            "AccountId",
            "AccountName",
            "AccountMarketingSegment",
            "AccountInvestmentObjectives",
            "AccountServiceModel",
            "OwnerId",
            "OwnerName",
            "OwnerState",
            "OwnerCity",
            "OwnerSmallPhotoUrl",
            "FinancialAccountType",
            "JointOwnerId",
            "Balance",
            "HeldAway",
            "RecordTypeName",
            "AccountTotalAUMPrimaryOwner",
            "AccountTotalFinAcctsPrimaryOwner",
            "AccountTotalHeldFinAcctsPrimaryOwner",
            "Managed",
            "Ownership"
        };
        
        return headerRecord;
    }

    public String[] getRowOfData(){
        String[] dataRecord = {
            this.getId(),
            this.getAccountId(),
            this.getAccountName(),
            this.getAccountMarketingSegment(),
            this.getAccountInvestmentObjectives(),
            this.getAccountServiceModel(),
            this.getOwnerId(),
            this.getOwnerName(),
            this.getOwnerState(),
            this.getOwnerCity(),
            this.getOwnerSmallPhotoUrl(),
            this.getFinancialAccountType(),
            this.getJointOwnerId(),
            Double.valueOf(this.getBalance()).toString(),
            Boolean.valueOf(this.getHeldAway()).toString(),
            this.getRecordTypeName(),
            Double.valueOf(this.getAccountTotalAUMPrimaryOwner()).toString(),
            Double.valueOf(this.getAccountTotalFinAcctsPrimaryOwner()).toString(),
            Double.valueOf(this.getAccountTotalHeldFinAcctsPrimaryOwner()).toString(),
            Boolean.valueOf(this.isManaged()).toString(),
            this.getOwnership()
        };
        
        return dataRecord;
    }

    public ArrayList<FinancialAccountTransactionCsv> getTransactions() {
        return this.transactions;
    }

    public void setTransactions(ArrayList<FinancialAccountTransactionCsv> transactions) {
        this.transactions = transactions;
    }

    public String getRecordTypeName() {
        return this.recordTypeName;
    }

    public void setRecordTypeName(String recordTypeName) {
        this.recordTypeName = recordTypeName;
    }

    public double getAccountTotalAUMPrimaryOwner() {
        return this.accountTotalAUMPrimaryOwner;
    }

    public void setAccountTotalAUMPrimaryOwner(double accountTotalAUMPrimaryOwner) {
        this.accountTotalAUMPrimaryOwner = accountTotalAUMPrimaryOwner;
    }

    public double getAccountTotalFinAcctsPrimaryOwner() {
        return this.accountTotalFinAcctsPrimaryOwner;
    }

    public void setAccountTotalFinAcctsPrimaryOwner(double accountTotalFinAcctsPrimaryOwner) {
        this.accountTotalFinAcctsPrimaryOwner = accountTotalFinAcctsPrimaryOwner;
    }

    public double getAccountTotalHeldFinAcctsPrimaryOwner() {
        return this.accountTotalHeldFinAcctsPrimaryOwner;
    }

    public void setAccountTotalHeldFinAcctsPrimaryOwner(double accountTotalHeldFinAcctsPrimaryOwner) {
        this.accountTotalHeldFinAcctsPrimaryOwner = accountTotalHeldFinAcctsPrimaryOwner;
    }

    public boolean isManaged() {
        return this.managed;
    }

    public boolean getManaged() {
        return this.managed;
    }

    public void setManaged(boolean managed) {
        this.managed = managed;
    }

    public String getOwnership() {
        return this.ownership;
    }

    public void setOwnership(String ownership) {
        this.ownership = ownership;
    }

    public String getOwnerId() {
        return this.ownerId;
    }

    public void setOwnerId(String ownerId) {
        this.ownerId = ownerId;
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

    public String getCreatedDate() {
        return this.createdDate;
    }

    public void setCreatedDate(String createdDate) {
        this.createdDate = createdDate;
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