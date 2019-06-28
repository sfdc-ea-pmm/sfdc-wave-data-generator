package pmmtech;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;

import com.opencsv.bean.CsvBindByName;

/**
 * AccountCsv
 */
public class AccountCsv {

    @CsvBindByName(column = "Name")
    private String name;

    @CsvBindByName(column = "InvestmentExperience")
    private String investmentExperience;

    @CsvBindByName(column = "InvestmentObjectives")
    private String investmentObjectives;

    @CsvBindByName(column = "AccountNumber")
    private String accountNumber;

    @CsvBindByName(column = "Id")
    private String id;

    @CsvBindByName(column = "RelationshipStartDate", required = false)
    private String relationshipStartDate;

    @CsvBindByName(column = "RecordTypeName", required = false)
    private String recordTypeName;

    @CsvBindByName(column = "OwnerId", required = false)
    private String ownerId;

    @CsvBindByName(column = "LeadOrContactId", required = false)
    private String leadOrContactId;

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

    @CsvBindByName(column = "ReviewFrequency", required = false)
    private String reviewFrequency;

    @CsvBindByName(column = "HouseholdSize", required = false)
    private int householdSize;

    @CsvBindByName(column = "HouseholdSizeText", required = false)
    private String householdSizeText;

    @CsvBindByName(column = "HouseholdComputed", required = false)
    private String householdComputed;

    @CsvBindByName(column = "RollupHouseHoldName", required = false)
    private String rollupHouseHoldName;

    @CsvBindByName(column = "MarketingSegment", required = false)
    private String marketingSegment;

    @CsvBindByName(column = "CustomerSegment", required = false)
    private String customerSegment;

    @CsvBindByName(column = "ServiceModel", required = false)
    private String serviceModel;

    @CsvBindByName(column = "LastReview", required = false)
    private String lastReview;

    @CsvBindByName(column = "LastInteraction", required = false)
    private String lastInteraction;

    @CsvBindByName(column = "NextReview", required = false)
    private String nextReview;

    @CsvBindByName(column = "Phone", required = false)
    private String phone;

    @CsvBindByName(column = "BillingState", required = false)
    private String billingState;

    @CsvBindByName(column = "BillingPostalCode", required = false)
    private String billingPostalCode;

    @CsvBindByName(column = "PrimaryContactAnnualIncome", required = false)
    private double primaryContactAnnualIncome;

    @CsvBindByName(column = "PrimaryContactGender", required = false)
    private String primaryContactGender;

    @CsvBindByName(column = "PrimaryContactEmail", required = false)
    private String primaryContactEmail;

    @CsvBindByName(column = "PrimaryContactAge", required = false)
    private int primaryContactAge;

    @CsvBindByName(column = "ClientCategory", required = false)
    private String clientCategory;

    @CsvBindByName(column = "ClientCategoryCustom", required = false)
    private String clientCategoryCustom;

    @CsvBindByName(column = "YearsSinceClient", required = false)
    private int yearsSinceClient;    

    @CsvBindByName(column = "TotalAUMPrimaryOwner", required = false)
    private double totalAUMPrimaryOwner;

    @CsvBindByName(column = "TotalAUMJointOwner", required = false)
    private double totalAUMJointOwner;
    
    @CsvBindByName(column = "TotalFinAcctsPrimaryOwner", required = false)
    private double totalFinAcctsPrimaryOwner;
    
    @CsvBindByName(column = "TotalFinAcctsJointOwner", required = false)
    private double totalFinAcctsJointOwner;
    
    @CsvBindByName(column = "TotalHeldFinAcctsPrimaryOwner", required = false)
    private double totalHeldFinAcctsPrimaryOwner;
    
    @CsvBindByName(column = "TotalHeldFinAcctsJointOwner", required = false)
    private double totalHeldFinAcctsJointOwner;
    
    @CsvBindByName(column = "TotalNumberOfFinAccountsPrimaryOwner", required = false)
    private double totalNumberOfFinAccountsPrimaryOwner;

    @CsvBindByName(column = "NetWorth", required = false)
    private double netWorth;

    @CsvBindByName(column = "AgeBucket", required = false)
    private String ageBucket;

    @CsvBindByName(column = "AUMBucket", required = false)
    private String aumBucket;

    @CsvBindByName(column = "YearsSinceClientBucket", required = false)
    private String yearsSinceClientBucket;

    @CsvBindByName(column = "NetWorthBucket", required = false)
    private String netWorthBucket;

    @CsvBindByName(column = "TotalFinancialAccounts", required = false)
    private double totalFinancialAccounts;

    @CsvBindByName(column = "HeldAway", required = false)
    private double heldAway;

    @CsvBindByName(column = "AUM", required = false)
    private double aum;

    @CsvBindByName(column = "AUA", required = false)
    private double aua;

    @CsvBindByName(column = "WalletShare", required = false)
    private double walletShare;

    @CsvBindByName(column = "FinancialInterests", required = false)
    private String financialInterests;

    @CsvBindByName(column = "BillingCountry", required = false)
    private String billingCountry;

    @CsvBindByName(column = "DaysSinceLastInteraction", required = false)
    private long daysSinceLastInteraction;

    @CsvBindByName(column = "CreatedDate", required = false)
    private String createdDate;

    @CsvBindByName(column = "RiskTolerance", required = false)
    private String riskTolerance;

    @CsvBindByName(column = "SampleAccount", required = false)
    private boolean sampleAccount;

    private boolean heldAwayWillIncrease;
    private String industry;
    private boolean willHaveReview;

    private ArrayList<FinancialAccountCsv> financialAccounts = new ArrayList<FinancialAccountCsv>();
    private ArrayList<ActivityCsv> activities = new ArrayList<ActivityCsv>();
    private ArrayList<CaseCsv> cases = new ArrayList<CaseCsv>();    

    /////////////////////////// Getters and Setters ///////////////////////////

    public String getName() {
        return this.name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getLeadOrContactId() {
        return this.leadOrContactId;
    }

    public void setLeadOrContactId(String leadOrContactId) {
        this.leadOrContactId = leadOrContactId;
    }


    public String getInvestmentExperience() {
        return this.investmentExperience;
    }

    public void setInvestmentExperience(String investmentExperience) {
        this.investmentExperience = investmentExperience;
    }

    public String getInvestmentObjectives() {
        return this.investmentObjectives;
    }

    public void setInvestmentObjectives(String investmentObjectives) {
        this.investmentObjectives = investmentObjectives;
    }

    public String getAccountNumber() {
        return this.accountNumber;
    }

    public void setAccountNumber(String accountNumber) {
        this.accountNumber = accountNumber;
    }

    public String getId() {
        return this.id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getRelationshipStartDate() {
        return this.relationshipStartDate;
    }

    public void setRelationshipStartDate(String relationshipStartDate) {
        this.relationshipStartDate = relationshipStartDate;
    }

    public String getRecordTypeName() {
        return this.recordTypeName;
    }

    public void setRecordTypeName(String recordTypeName) {
        this.recordTypeName = recordTypeName;
    }

    public String getOwnerName() {
        return this.ownerName;
    }

    public void setOwnerName(String ownerName) {
        this.ownerName = ownerName;
    }

    public String getMarketingSegment() {
        return this.marketingSegment;
    }

    public void setMarketingSegment(String marketingSegment) {
        this.marketingSegment = marketingSegment;
    }

    public String getCustomerSegment() {
        return this.customerSegment;
    }

    public void setCustomerSegment(String customerSegment) {
        this.customerSegment = customerSegment;
    }

    public String getServiceModel() {
        return this.serviceModel;
    }

    public void setServiceModel(String serviceModel) {
        this.serviceModel = serviceModel;
    }

    public String getLastReview() {
        return this.lastReview;
    }

    public void setLastReview(String lastReview) {
        this.lastReview = lastReview;
    }

    public String getLastInteraction() {
        return this.lastInteraction;
    }

    public void setLastInteraction(String lastInteraction) {
        this.lastInteraction = lastInteraction;
    }

    public String getNextReview() {
        return this.nextReview;
    }

    public void setNextReview(String nextReview) {
        this.nextReview = nextReview;
    }

    public String getPhone() {
        return this.phone;
    }

    public void setPhone(String phone) {
        this.phone = phone;
    }

    public String getBillingState() {
        return this.billingState;
    }

    public void setBillingState(String billingState) {
        this.billingState = billingState;
    }

    public String getBillingPostalCode() {
        return this.billingPostalCode;
    }

    public void setBillingPostalCode(String billingPostalCode) {
        this.billingPostalCode = billingPostalCode;
    }

    public double getPrimaryContactAnnualIncome() {
        return this.primaryContactAnnualIncome;
    }

    public void setPrimaryContactAnnualIncome(double primaryContactAnnualIncome) {
        this.primaryContactAnnualIncome = primaryContactAnnualIncome;
    }

    public String getPrimaryContactGender() {
        return this.primaryContactGender;
    }

    public void setPrimaryContactGender(String primaryContactGender) {
        this.primaryContactGender = primaryContactGender;
    }

    public String getPrimaryContactEmail() {
        return this.primaryContactEmail;
    }

    public void setPrimaryContactEmail(String primaryContactEmail) {
        this.primaryContactEmail = primaryContactEmail;
    }

    public int getPrimaryContactAge() {
        return this.primaryContactAge;
    }

    public void setPrimaryContactAge(int primaryContactAge) {
        this.primaryContactAge = primaryContactAge;
    }

    public String getClientCategory() {
        return this.clientCategory;
    }

    public void setClientCategory(String clientCategory) {
        this.clientCategory = clientCategory;
    }

    public String getClientCategoryCustom() {
        /*
         * case when 'FinServ__ClientCategory__c' == \"Platinum\" then \"1 - Platinum\"
         * when 'FinServ__ClientCategory__c' == \"Gold\" then \"2 - Gold\" when
         * 'FinServ__ClientCategory__c' == \"Silver\" then \"3 - Silver\" when
         * 'FinServ__ClientCategory__c' == \"Bronze\" then \"4 - Bronze\" else
         * \"5 - Standard\" end
         */
        String customCat = "";

        switch (this.clientCategory) {
        case "Platinum":
            customCat = "1 - Platinum";
            break;

        case "Gold":
            customCat = "2 - Gold";
            break;

        case "Silver":
            customCat = "3 - Silver";
            break;

        case "Bronze":
            customCat = "4 - Bronze";
            break;
        default:
            customCat = "5 - Standard";
            break;
        }

        return customCat;
    }

    public String getAgeBucket() {
        /*
         * case when string_to_number('FinServ__PrimaryContact__c.FinServ__Age__c') < 18
         * then \"1. < 18\" when
         * string_to_number('FinServ__PrimaryContact__c.FinServ__Age__c') >= 18 &&
         * string_to_number('FinServ__PrimaryContact__c.FinServ__Age__c') <= 29 then
         * \"2. 18-29\" when
         * string_to_number('FinServ__PrimaryContact__c.FinServ__Age__c') > 29 &&
         * string_to_number('FinServ__PrimaryContact__c.FinServ__Age__c') <= 49 then
         * \"3. 30-49\" when
         * string_to_number('FinServ__PrimaryContact__c.FinServ__Age__c') > 49 &&
         * string_to_number('FinServ__PrimaryContact__c.FinServ__Age__c') <= 69 then
         * \"4. 50-69\" when
         * string_to_number('FinServ__PrimaryContact__c.FinServ__Age__c') > 69 then
         * \"5. > 69\" else \"6. NA\" end
         */
        String age = "";

        if (this.primaryContactAge < 18) {
            age = "1. < 18";
        } else if (this.primaryContactAge >= 18 && this.primaryContactAge <= 29) {
            age = "2. 18-29";
        } else if (this.primaryContactAge >= 30 && this.primaryContactAge <= 49) {
            age = "3. 30-49";
        } else if (this.primaryContactAge >= 50 && this.primaryContactAge <= 69) {
            age = "4. 50-69";
        } else if (this.primaryContactAge > 69) {
            age = "5. > 69";
        } else {
            age = "6. NA";
        }

        return age;
    }
	public int getYearsSinceClient() {
        return this.yearsSinceClient;
    }

    public void setYearsSinceClient(int yearsSinceClient) {
        this.yearsSinceClient = yearsSinceClient;
    }

    public String getYearsSinceClientBucket(){
        /*
        case when 'YearsSinceClient' < 1 then \"1. Less than 1 year\" 
        when 'YearsSinceClient' >= 1 && 'YearsSinceClient' < 3 then \"2. Between 1 and 3 years\" 
        when 'YearsSinceClient' >= 3 && 'YearsSinceClient' < 5 then \"3. Between 3 and 5 years\" 
        when 'YearsSinceClient' >= 5 && 'YearsSinceClient' < 10 then \"4. Between 5 and 10 Years\" 
        when 'YearsSinceClient' >= 10 && 'YearsSinceClient' < 15 then \"5. Between 10 and 15 years\" 
        when 'YearsSinceClient' >= 15 then \"6. Greater than 15Y\" end
        */

        String age = "";

        if (this.yearsSinceClient < 1) {
            age = "1. Less than 1 year";
        } 
        else if (this.yearsSinceClient >= 1 && this.yearsSinceClient < 3) {
            age = "2. Between 1 and 3 years";
        } 
        else if (this.yearsSinceClient >= 3 && this.yearsSinceClient < 5) {
            age = "3. Between 3 and 5 years";
        } 
        else if (this.yearsSinceClient >= 5 && this.yearsSinceClient < 10) {
            age = "4. Between 5 and 10 Years";
        }
        else if (this.yearsSinceClient >= 10 && this.yearsSinceClient < 15) {
            age = "5. Between 10 and 15 years";
        } 
        else if (this.yearsSinceClient >= 15) {
            age = "6. Greater than 15Y";
        }
        else {
            age = "7. NA";
        }

        return age;
    }

	public void setClientCategoryCustom(String clientCategoryCustom) {
        this.clientCategoryCustom = clientCategoryCustom;
    }

    public double getTotalAUMPrimaryOwner() {
        return this.totalAUMPrimaryOwner;
    }

    public void setTotalAUMPrimaryOwner(double totalAUMPrimaryOwner) {
        this.totalAUMPrimaryOwner = totalAUMPrimaryOwner;
    }

    public double getTotalAUMJointOwner() {
        return this.totalAUMJointOwner;
    }

    public void setTotalAUMJointOwner(double totalAUMJointOwner) {
        this.totalAUMJointOwner = totalAUMJointOwner;
    }

    public double getTotalFinAcctsPrimaryOwner() {
        return this.totalFinAcctsPrimaryOwner;
    }

    public void setTotalFinAcctsPrimaryOwner(double totalFinAcctsPrimaryOwner) {
        this.totalFinAcctsPrimaryOwner = totalFinAcctsPrimaryOwner;
    }

    public double getTotalFinAcctsJointOwner() {
        return this.totalFinAcctsJointOwner;
    }

    public void setTotalFinAcctsJointOwner(double totalFinAcctsJointOwner) {
        this.totalFinAcctsJointOwner = totalFinAcctsJointOwner;
    }

    public double getTotalHeldFinAcctsPrimaryOwner() {
        return this.totalHeldFinAcctsPrimaryOwner;
    }

    public void setTotalHeldFinAcctsPrimaryOwner(double totalHeldFinAcctsPrimaryOwner) {
        this.totalHeldFinAcctsPrimaryOwner = totalHeldFinAcctsPrimaryOwner;
    }

    public double getTotalHeldFinAcctsJointOwner() {
        return this.totalHeldFinAcctsJointOwner;
    }

    public void setTotalHeldFinAcctsJointOwner(double totalHeldFinAcctsJointOwner) {
        this.totalHeldFinAcctsJointOwner = totalHeldFinAcctsJointOwner;
    }

    public double getTotalNumberOfFinAccountsPrimaryOwner() {
        return this.totalNumberOfFinAccountsPrimaryOwner;
    }

    public void setTotalNumberOfFinAccountsPrimaryOwner(double totalNumberOfFinAccountsPrimaryOwner) {
        this.totalNumberOfFinAccountsPrimaryOwner = totalNumberOfFinAccountsPrimaryOwner;
    }

    public double getNetWorth() {
        //return this.netWorth;
        double worth = this.getAum() + this.getHeldAway();
        return worth;
    }

    public void setNetWorth(double netWorth) {
        this.netWorth = netWorth;
    }

    public String getNetWorthBucket(){
        /*
        case when 'FinServ__NetWorth__c' > 0 && 'FinServ__NetWorth__c' < 500000 then \"1. Less than 500K\" 
        when 'FinServ__NetWorth__c' >= 500000 && 'FinServ__NetWorth__c' < 2000000 then \"2. Between 500K and 2M\" 
        when 'FinServ__NetWorth__c' >= 2000000 && 'FinServ__NetWorth__c' < 5000000 then \"3. Between 2M and 5M\" 
        when 'FinServ__NetWorth__c' >= 5000000 && 'FinServ__NetWorth__c' < 10000000 then \"4. Between 5M and 10M\" 
        when 'FinServ__NetWorth__c' >= 10000000 then \"5. More than 10M\" 
        else \"6. NA\" end
        */

        String nw = "";
        double thisNW = this.getNetWorth();

        if (thisNW > 0 && thisNW < 500000) {
            nw = "1. Less than 500K";
        } 
        else if (thisNW >= 500000 && thisNW < 2000000) {
            nw = "2. Between 500K and 2M";
        } 
        else if (thisNW >= 2000000 && thisNW < 5000000) {
            nw = "3. Between 2M and 5M";
        } 
        else if (thisNW >= 5000000 && thisNW < 10000000) {
            nw = "4. Between 5M and 10M";
        }
        else if (thisNW >= 10000000) {
            nw = "5. More than 10M";
        }
        else {
            nw = "6. NA";
        }

        return nw;
    }

    public double getTotalFinancialAccounts(){
        return this.totalFinAcctsPrimaryOwner + this.totalFinAcctsJointOwner;
    }

    public double getHeldAway(){
        //this.getTotalFinancialAccounts() - this.totalHeldFinAcctsPrimaryOwner - this.totalHeldFinAcctsJointOwner
        return this.totalHeldFinAcctsPrimaryOwner + this.totalHeldFinAcctsJointOwner;
    }

    public double getAum(){
        return this.totalAUMPrimaryOwner + this.totalAUMJointOwner;
    }

    public double getAua(){
        // this.getTotalFinancialAccounts() - this.getAum() - this.getHeldAway();
        return this.getHeldAway();
    }

    public double getWalletShare(){
        double divided = this.getHeldAway();
        double divisor = this.getTotalFinancialAccounts() == 0 ? 1 : getTotalFinancialAccounts();

        return divided / divisor;
    }

    public static String[] getCsvHeader(){
        String[] headerRecord = {
            "Name",
            "InvestmentExperience",
            "InvestmentObjectives",
            "AccountNumber",
            "Id",
            "LeadOrContactId",
            "RelationshipStartDate",
            "RecordTypeName",
            "OwnerId",
            "OwnerName",
            "OwnerState",
            "OwnerCity",
            "OwnerRoleName",
            "OwnerEmail",
            "OwnerSmallPhotoUrl",
            "MarketingSegment",
            "CustomerSegment",
            "ServiceModel",
            "LastReview",
            "LastInteraction",
            "NextReview",
            "Phone",
            "BillingState",
            "BillingPostalCode",
            "PrimaryContactAnnualIncome",
            "PrimaryContactGender",
            "PrimaryContactEmail",
            "PrimaryContactAge",
            "ClientCategory",
            "ClientCategoryCustom",
            "YearsSinceClient",
            "TotalAUMPrimaryOwner",
            "TotalAUMJointOwner",
            "TotalFinAcctsPrimaryOwner",
            "TotalFinAcctsJointOwner",
            "TotalHeldFinAcctsPrimaryOwner",
            "TotalHeldFinAcctsJointOwner",
            "TotalNumberOfFinAccountsPrimaryOwner",
            "NetWorth",
            "AgeBucket",
            "YearsSinceClientBucket",
            "NetWorthBucket",
            "TotalFinancialAccounts",
            "HeldAway",
            "AUM",
            "AUA",
            "WalletShare",
            "SampleAccount"
        };
        
        return headerRecord;
    }

    public String[] getRowOfData(){
        String[] dataRecord = {
            this.getName(),
            this.getInvestmentExperience(),
            this.getInvestmentObjectives(),
            this.getAccountNumber(),
            this.getId(),
            this.getLeadOrContactId(),
            this.getRelationshipStartDate(),
            this.getRecordTypeName(),
            this.getOwnerId(),
            this.getOwnerName(),
            this.getOwnerState(),
            this.getOwnerCity(),
            this.getOwnerRoleName(),
            this.getOwnerEmail(),
            this.getOwnerSmallPhotoUrl(),
            this.getMarketingSegment(),
            this.getCustomerSegment(),
            this.getServiceModel(),
            this.getLastReview(),
            this.getLastInteraction(),
            this.getNextReview(),
            this.getPhone(),
            this.getBillingState(),
            this.getBillingPostalCode(),
            Double.valueOf(this.getPrimaryContactAnnualIncome()).toString(),
            this.getPrimaryContactGender(),
            this.getPrimaryContactEmail(),
            Integer.valueOf(this.getPrimaryContactAge()).toString(),
            this.getClientCategory(),
            this.getClientCategoryCustom(),
            Double.valueOf(this.getYearsSinceClient()).toString(),
            Double.valueOf(this.getTotalAUMPrimaryOwner()).toString(),
            Double.valueOf(this.getTotalAUMJointOwner()).toString(),
            Double.valueOf(this.getTotalFinAcctsPrimaryOwner()).toString(),
            Double.valueOf(this.getTotalFinAcctsJointOwner()).toString(),
            Double.valueOf(this.getTotalHeldFinAcctsPrimaryOwner()).toString(),
            Double.valueOf(this.getTotalHeldFinAcctsJointOwner()).toString(),
            Double.valueOf(this.getTotalNumberOfFinAccountsPrimaryOwner()).toString(),
            Double.valueOf(this.getNetWorth()).toString(),
            this.getAgeBucket(),
            this.getYearsSinceClientBucket(),
            this.getNetWorthBucket(),
            Double.valueOf(this.getTotalFinancialAccounts()).toString(),
            Double.valueOf(this.getHeldAway()).toString(),
            Double.valueOf(this.getAum()).toString(),
            Double.valueOf(this.getAua()).toString(),
            Double.valueOf(this.getWalletShare()).toString(),
            Boolean.valueOf(this.isSampleAccount()).toString()
        };
        
        return dataRecord;
    }
	
    public ArrayList<FinancialAccountCsv> getFinancialAccounts() {
        return this.financialAccounts;
    }

    public void setFinancialAccounts(ArrayList<FinancialAccountCsv> financialAccounts) {
        this.financialAccounts = financialAccounts;
    }

    public ArrayList<FinancialAccountCsv> getHeldAwayFinancialAccounts() {
        ArrayList<FinancialAccountCsv> heldAwayFinAccts = new ArrayList<FinancialAccountCsv>();
        for (FinancialAccountCsv var : this.financialAccounts) {
            if (var.isHeldAway()) {
                heldAwayFinAccts.add(var);
            }
        }
        return heldAwayFinAccts;
    }

    public ArrayList<ActivityCsv> getActivities() {
        return this.activities;
    }

    public void setActivities(ArrayList<ActivityCsv> activities) {
        this.activities = activities;
    }

    public ArrayList<CaseCsv> getCases() {
        return this.cases;
    }

    public void setCases(ArrayList<CaseCsv> cases) {
        this.cases = cases;
    }

    public boolean getHeldAwayWillIncrease() {
        return this.heldAwayWillIncrease;
    }

    public void setHeldAwayWillIncrease(boolean heldAwayWillIncrease) {
        this.heldAwayWillIncrease = heldAwayWillIncrease;
    }

    public String getIndustry() {
        return this.industry;
    }

    public void setIndustry(String industry) {
        this.industry = industry;
    }

    public boolean isSampleAccount() {
        return this.sampleAccount;
    }

    public boolean getSampleAccount() {
        return this.sampleAccount;
    }

    public void setSampleAccount(boolean sampleAccount) {
        this.sampleAccount = sampleAccount;
    }

    public String getOwnerId() {
        return this.ownerId;
    }

    public void setOwnerId(String ownerId) {
        this.ownerId = ownerId;
    }

    public String getFinancialInterests() {
        return this.financialInterests;
    }

    public void setFinancialInterests(String financialInterests) {
        this.financialInterests = financialInterests;
    }

    public String getBillingCountry() {
        return this.billingCountry;
    }

    public void setBillingCountry(String billingCountry) {
        this.billingCountry = billingCountry;
    }

    public long getDaysSinceLastInteraction() {

        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
        try {
            Date lastIntDate = sdf.parse(this.lastInteraction);
            Calendar calNow = Calendar.getInstance();
            Date actDate = calNow.getTime();
            this.daysSinceLastInteraction = Helper.getDaysBetween(lastIntDate, actDate);
        }
        catch (ParseException e) {
            this.daysSinceLastInteraction = 0;
        }

        if(this.daysSinceLastInteraction < 0){
            this.daysSinceLastInteraction = 0;
        }

        return this.daysSinceLastInteraction;
    }

    public void setDaysSinceLastInteraction(long daysSinceLastInteraction) {
        this.daysSinceLastInteraction = daysSinceLastInteraction;
    }

    public String getCreatedDate() {
        return this.createdDate;
    }

    public void setCreatedDate(String createdDate) {
        this.createdDate = createdDate;
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

    public String getReviewFrequency() {
        return this.reviewFrequency;
    }

    public void setReviewFrequency(String reviewFrequency) {
        this.reviewFrequency = reviewFrequency;
    }

    public int getHouseholdSize() {
        return this.householdSize;
    }

    public void setHouseholdSize(int householdSize) {
        this.householdSize = householdSize;
    }

    public String getHouseholdSizeText() {
        return this.householdSizeText;
    }

    public void setHouseholdSizeText(String householdSizeText) {
        this.householdSizeText = householdSizeText;
    }

    public String getHouseholdComputed() {
        return this.householdComputed;
    }

    public void setHouseholdComputed(String householdComputed) {
        this.householdComputed = householdComputed;
    }

    public String getRollupHouseHoldName() {
        return this.rollupHouseHoldName;
    }

    public void setRollupHouseHoldName(String rollupHouseHoldName) {
        this.rollupHouseHoldName = rollupHouseHoldName;
    }

    public String getAumBucket() {
        /* 
        case when 'FinServ__AUM__c' > 0 && 'FinServ__AUM__c' < 500000 then \"1. Less than 500K\" 
        when 'FinServ__AUM__c' >= 500000 && 'FinServ__AUM__c' < 2000000 then \"2. Between 500K and 2M\" 
        when 'FinServ__AUM__c' >= 2000000 && 'FinServ__AUM__c' < 5000000 then \"3. Between 2M and 5M\" 
        when 'FinServ__AUM__c' >= 5000000 && 'FinServ__AUM__c' < 10000000 then \"4. Between 5M and 10M\" 
        when 'FinServ__AUM__c' >= 10000000 then \"5. More than 10M\" 
        else \"6. NA\" end
        */

        double aumVal = this.getAum();

        if (aumVal > 0 && aumVal < 500000) {
            this.aumBucket = "1. Less than 500K";
        } 
        else if(aumVal >= 500000 && aumVal < 2000000){
            this.aumBucket = "2. Between 500K and 2M";
        }
        else if(aumVal >= 2000000 && aumVal < 5000000){
            this.aumBucket = "3. Between 2M and 5M";
        }
        else if(aumVal >= 5000000 && aumVal < 10000000){
            this.aumBucket = "4. Between 5M and 10M";
        }
        else if(aumVal >= 10000000 && aumVal < 10000000){
            this.aumBucket = "5. More than 10M";
        }
        else {
            this.aumBucket = "6. NA";
        }

        return this.aumBucket;
    }

    public void setAumBucket(String aumBucket) {
        this.aumBucket = aumBucket;
    }

    public String getRiskTolerance() {
        return this.riskTolerance;
    }

    public void setRiskTolerance(String riskTolerance) {
        this.riskTolerance = riskTolerance;
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

    public boolean getWillHaveReview() {
        return this.willHaveReview;
    }

    public void setWillHaveReview(boolean willHaveReview) {
        this.willHaveReview = willHaveReview;
    }    

    public void generateReviewAndInteractionDates(Calendar relativeDate){
        // FinServ__LastReview__c (Random date between today and -1 month)
        // FinServ__LastInteraction__c (Random date between today and FinServ__LastReview__c)
        // FinServ__NextReview__c (Today() + Random days 1, 30)
        
        int daysSinceLastReview = Helper.getRandomNumberInRange(1, 30);
        int daysSinceLastInteraction = Helper.getRandomNumberInRange(0, daysSinceLastReview);
        int daysUntilNextReview = Helper.getRandomNumberInRange(15, 30);

        Calendar calLastReviewDate = (Calendar)relativeDate.clone();
        Calendar calLastInteractionDate = (Calendar)relativeDate.clone();
        Calendar calNextReviewDate = (Calendar)relativeDate.clone();

        calLastReviewDate.add(Calendar.DAY_OF_MONTH, -daysSinceLastReview);
        calLastInteractionDate.add(Calendar.DAY_OF_MONTH, -daysSinceLastInteraction);
        calNextReviewDate.add(Calendar.DAY_OF_MONTH, daysUntilNextReview);
        
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
        this.setLastReview(sdf.format(calLastReviewDate.getTime()));
        this.setLastInteraction(sdf.format(calLastInteractionDate.getTime()));
        this.setNextReview(sdf.format(calNextReviewDate.getTime()));
    }
}