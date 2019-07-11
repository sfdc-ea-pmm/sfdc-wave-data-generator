package pmmtech;

import com.opencsv.bean.CsvBindByName;

/**
 * FinancialAccountTransactionCsv
 */
public class FinancialAccountTransactionCsv {

    @CsvBindByName(column = "Id")
    private String id;

    @CsvBindByName(column = "AccountId")
    private String accountId;

    @CsvBindByName(column = "AccountName")
    private String accountName;

    @CsvBindByName(column = "AccountPrimaryContactName")
    private String accountPrimaryContactName;

    @CsvBindByName(column = "AccountMarketingSegment")
    private String accountMarketingSegment;

    @CsvBindByName(column = "AccountInvestmentObjectives")
    private String accountInvestmentObjectives;

    @CsvBindByName(column = "AccountInvestmentExperience")
    private String accountInvestmentExperience;

    @CsvBindByName(column = "AccountServiceModel")
    private String accountServiceModel;

    @CsvBindByName(column = "OwnerName")
    private String ownerName;

    @CsvBindByName(column = "AccountLastInteraction")
    private String accountLastInteraction;

    @CsvBindByName(column = "FinancialAccountType")
    private String financialAccountType;    

    @CsvBindByName(column = "Amount")
    private double amount;

    @CsvBindByName(column = "FinancialAccountId")
    private String financialAccountId;

    @CsvBindByName(column = "TransactionType")
    private String transactionType;

    @CsvBindByName(column = "TransactionDate")
    private String transactionDate;

    public void setAccountData(AccountCsv accountData){
        this.setAccountId(accountData.getId());
        this.setAccountInvestmentObjectives(accountData.getInvestmentObjectives());
        this.setAccountInvestmentExperience(accountData.getInvestmentExperience());
        this.setAccountMarketingSegment(accountData.getMarketingSegment());
        this.setAccountName(accountData.getName());
        this.setAccountServiceModel(accountData.getServiceModel());
        this.setAccountPrimaryContactName(accountData.getPrimaryContactEmail());
        this.setAccountLastInteraction(accountData.getLastInteraction());
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

    public String getAccountPrimaryContactName() {
        return this.accountPrimaryContactName;
    }

    public void setAccountPrimaryContactName(String accountPrimaryContactName) {
        this.accountPrimaryContactName = accountPrimaryContactName;
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

    public double getAmount() {
        return this.amount;
    }

    public double getArithmeticAmount(){
        
        double arithmeticAmount = 0;
        
        switch (this.transactionType) {
            case "Debit":
                arithmeticAmount = -this.amount;        
                break;
        
            default:
                arithmeticAmount = this.amount;
                break;
        }

        return arithmeticAmount;
    }

    public void setAmount(double amount) {
        this.amount = amount;
    }

    public String getFinancialAccountId() {
        return this.financialAccountId;
    }

    public void setFinancialAccountId(String financialAccountId) {
        this.financialAccountId = financialAccountId;
    }

    public String getTransactionType() {
        return this.transactionType;
    }

    public void setTransactionType(String transactionType) {
        this.transactionType = transactionType;
    }

    public String getTransactionDate() {
        return this.transactionDate;
    }

    public void setTransactionDate(String transactionDate) {
        this.transactionDate = transactionDate;
    }

    public static String[] getCsvHeader(){
        String[] headerRecord = {
            "Id",
            "AccountId",
            "AccountName",
            "AccountPrimaryContactName",
            "AccountMarketingSegment",
            "AccountInvestmentObjectives",
            "AccountInvestmentExperience",
            "AccountLastInteraction",
            "AccountServiceModel",
            "OwnerName",
            "FinancialAccountType",
            "Amount",
            "FinancialAccountId",
            "TransactionType",
            "TransactionDate"
        };
        
        return headerRecord;
    }

    public String[] getRowOfData(){
        String[] dataRecord = {
            this.getId(),
            this.getAccountId(),
            this.getAccountName(),
            this.getAccountPrimaryContactName(),
            this.getAccountMarketingSegment(),
            this.getAccountInvestmentObjectives(),
            this.getAccountInvestmentExperience(),
            this.getAccountLastInteraction(),
            this.getAccountServiceModel(),
            this.getOwnerName(),
            this.getFinancialAccountType(),
            Double.valueOf(this.getAmount()).toString(),
            this.getFinancialAccountId(),
            this.getTransactionType(),
            this.getTransactionDate()
        };
        
        return dataRecord;
    }
    

    public String getAccountInvestmentExperience() {
        return this.accountInvestmentExperience;
    }

    public void setAccountInvestmentExperience(String accountInvestmentExperience) {
        this.accountInvestmentExperience = accountInvestmentExperience;
    }

    public String getAccountLastInteraction() {
        return this.accountLastInteraction;
    }

    public void setAccountLastInteraction(String accountLastInteraction) {
        this.accountLastInteraction = accountLastInteraction;
    }

}