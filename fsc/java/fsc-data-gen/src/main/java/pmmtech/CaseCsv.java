package pmmtech;

import com.opencsv.bean.CsvBindByName;

/**
 * CaseCsv
 */
public class CaseCsv {

    @CsvBindByName(column = "Id")
    private String id;

    @CsvBindByName(column = "AccountId")
    private String accountId;

    @CsvBindByName(column = "AccountName")
    private String accountName;

    @CsvBindByName(column = "AccountServiceModel")
    private String accountServiceModel;

    @CsvBindByName(column = "AccountMarketingSegment")
    private String accountMarketingSegment;

    @CsvBindByName(column = "AccountInvestmentObjectives")
    private String accountInvestmentObjectives;

    @CsvBindByName(column = "AccountLastInteraction")
    private String accountLastInteraction;

    @CsvBindByName(column = "CreatedDate")
    private String createdDate;

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

    public String getAccountLastInteraction() {
        return this.accountLastInteraction;
    }

    public void setAccountLastInteraction(String accountLastInteraction) {
        this.accountLastInteraction = accountLastInteraction;
    }

    public String getCreatedDate() {
        return this.createdDate;
    }

    public void setCreatedDate(String createdDate) {
        this.createdDate = createdDate;
    }


    public String getAccountServiceModel() {
        return this.accountServiceModel;
    }

    public void setAccountServiceModel(String accountServiceModel) {
        this.accountServiceModel = accountServiceModel;
    }

    public void setAccountData(AccountCsv accountData){
        this.setAccountId(accountData.getId());
        this.setAccountInvestmentObjectives(accountData.getInvestmentObjectives());
        this.setAccountMarketingSegment(accountData.getMarketingSegment());
        this.setAccountName(accountData.getName());
        this.setAccountLastInteraction(accountData.getLastInteraction());
        this.setAccountServiceModel(accountData.getServiceModel());
    }
}