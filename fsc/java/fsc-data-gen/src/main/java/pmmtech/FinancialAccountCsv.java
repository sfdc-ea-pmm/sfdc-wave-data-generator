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

    @CsvBindByName(column = "OwnerName")
    private String ownerName;

    @CsvBindByName(column = "FinancialAccountType")
    private String financialAccountType;

    @CsvBindByName(column = "JointOwnerId")
    private String jointOwnerId;

    @CsvBindByName(column = "Balance")
    private double balance;

    @CsvBindByName(column = "HeldAway")
    private boolean heldAway;

    @CsvBindByName(column = "RecordTypeName")
    private String recordTypeName;

    private ArrayList<FinancialAccountTransactionCsv> transactions = new ArrayList<FinancialAccountTransactionCsv>();

    public void setAccountData(AccountCsv accountData){
        this.setAccountId(accountData.getId());
        this.setAccountInvestmentObjectives(accountData.getInvestmentObjectives());
        this.setAccountMarketingSegment(accountData.getMarketingSegment());
        this.setAccountName(accountData.getName());
        this.setAccountServiceModel(accountData.getServiceModel());        
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
            "OwnerName",
            "FinancialAccountType",
            "JointOwnerId",
            "Balance",
            "HeldAway",
            "RecordTypeName"
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
            this.getOwnerName(),
            this.getFinancialAccountType(),
            this.getJointOwnerId(),
            Double.valueOf(this.getBalance()).toString(),
            Boolean.valueOf(this.getHeldAway()).toString(),
            this.getRecordTypeName()
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

}