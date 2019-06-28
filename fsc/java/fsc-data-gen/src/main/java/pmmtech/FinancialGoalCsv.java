package pmmtech;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;

import com.opencsv.bean.CsvBindByName;

/**
 * FinancialGoalCsv
 */
public class FinancialGoalCsv {

    @CsvBindByName(column = "Id")
    private String id;

    @CsvBindByName(column = "CreatedDate")
    private String createdDate;

    @CsvBindByName(column = "AccountId")
    private String accountId;

    @CsvBindByName(column = "AccountName")
    private String accountName;

    @CsvBindByName(column = "AccountOwnerName")
    private String accountOwnerName;

    @CsvBindByName(column = "AccountInvestmentObjectives")
    private String accountInvestmentObjectives;

    @CsvBindByName(column = "AccountMarketingSegment")
    private String accountMarketingSegment;

    @CsvBindByName(column = "AccountServiceModel")
    private String accountServiceModel;

    @CsvBindByName(column = "AccountLastInteraction")
    private String accountLastInteraction;

    @CsvBindByName(column = "Name")
    private String name;

    @CsvBindByName(column = "AchievedPercentage")
    private double achievedPercentage;

    @CsvBindByName(column = "AchievedPercentageRange")
    private String achievedPercentageRange;

    @CsvBindByName(column = "ActualValue")
    private int actualValue;

    @CsvBindByName(column = "TargetValue")
    private int targetValue;

    private int finalActualValue;

    @CsvBindByName(column = "TargetDate")
    private String targetDate;

    @CsvBindByName(column = "Type")
    private String type;

    @CsvBindByName(column = "YearsUntilTarget")
    private int yearsUntilTarget;

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

    public void setAccountData(AccountCsv accData) {
        this.accountId = accData.getId();
        this.accountInvestmentObjectives = accData.getInvestmentObjectives();
        this.accountLastInteraction = accData.getLastInteraction();
        this.accountMarketingSegment = accData.getMarketingSegment();
        this.accountName = accData.getName();
        this.accountOwnerName = accData.getOwnerName();
        this.accountServiceModel = accData.getServiceModel();
    }

    public String getId() {
        return this.id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getCreatedDate() {
        return this.createdDate;
    }

    public void setCreatedDate(String createdDate) {
        this.createdDate = createdDate;
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

    public String getAccountOwnerName() {
        return this.accountOwnerName;
    }

    public void setAccountOwnerName(String accountOwnerName) {
        this.accountOwnerName = accountOwnerName;
    }

    public String getAccountInvestmentObjectives() {
        return this.accountInvestmentObjectives;
    }

    public void setAccountInvestmentObjectives(String accountInvestmentObjectives) {
        this.accountInvestmentObjectives = accountInvestmentObjectives;
    }

    public String getAccountMarketingSegment() {
        return this.accountMarketingSegment;
    }

    public void setAccountMarketingSegment(String accountMarketingSegment) {
        this.accountMarketingSegment = accountMarketingSegment;
    }

    public String getAccountLastInteraction() {
        return this.accountLastInteraction;
    }

    public void setAccountLastInteraction(String accountLastInteraction) {
        this.accountLastInteraction = accountLastInteraction;
    }

    public String getName() {
        return this.name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public double getAchievedPercentage() {
        return ((double)this.actualValue / this.targetValue) * 100;
    }

    public void setAchievedPercentage(double achievedPercentage) {
        this.achievedPercentage = achievedPercentage;
    }

    public String getAchievedPercentageRange() {
        // case when 'AchievedPercentage' == 0 then \"1. Not Started\" 
        // when 'AchievedPercentage' > 0 && 'AchievedPercentage' <= 26 then \"2. <=25%\" 
        // when 'AchievedPercentage' > 25 && 'AchievedPercentage' <= 50 then \"3. 26-50%\" 
        // when 'AchievedPercentage' > 50 && 'AchievedPercentage' <= 75 then \"4. 51-75%\" 
        // when 'AchievedPercentage' > 75 && 'AchievedPercentage' < 100 then \"5. 76-99%\" 
        // when 'AchievedPercentage' >= 100 then \"6. Completed\" end

        String prcRange = "1. Not Started";
        double achPrc = this.getAchievedPercentage();

        if (achPrc == 0) {
            prcRange = "1. Not Started";
        } 
        else if(achPrc > 0 && achPrc <= 26) {
            prcRange = "2. <=25%";
        }
        else if(achPrc > 25 && achPrc <= 50) {
            prcRange = "3. 26-50%";
        }
        else if(achPrc > 50 && achPrc <= 75) {
            prcRange = "4. 51-75%";
        }
        else if(achPrc > 75 && achPrc < 100) {
            prcRange = "5. 76-99%";
        }
        else {
            prcRange = "6. Completed";
        }

        return prcRange;
    }

    public int getActualValue() {
        return this.actualValue;
    }

    public void setActualValue(int actualValue) {
        this.actualValue = actualValue;
    }

    public int getTargetValue() {
        return this.targetValue;
    }

    public void setTargetValue(int targetValue) {
        this.targetValue = targetValue;
    }

    public String getTargetDate() {
        return this.targetDate;
    }

    public void setTargetDate(String targetDate) {
        this.targetDate = targetDate;
    }

    public String getType() {
        return this.type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public int getYearsUntilTarget() {

        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
        try {
            Date trgDate = sdf.parse(this.targetDate);
            Calendar calNow = Calendar.getInstance();
            Date actDate = calNow.getTime();
            this.yearsUntilTarget = Helper.getDiffYears(actDate, trgDate);
        }
        catch (ParseException e) {
            this.yearsUntilTarget = 0;
        }

        if(this.yearsUntilTarget < 0){
            this.yearsUntilTarget = 0;
        }

        return this.yearsUntilTarget;
    }

	public void setYearsUntilTarget(int yearsUntilTarget) {
        this.yearsUntilTarget = yearsUntilTarget;
    }

    public String getAccountServiceModel() {
        return this.accountServiceModel;
    }

    public void setAccountServiceModel(String accountServiceModel) {
        this.accountServiceModel = accountServiceModel;
    }

    public int getFinalActualValue() {
        return this.finalActualValue;
    }

    public void setFinalActualValue(int finalActualValue) {
        this.finalActualValue = finalActualValue;
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

	public void setAchievedPercentageRange(String achievedPercentageRange) {
        this.achievedPercentageRange = achievedPercentageRange;
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

    public static String[] getCsvHeader(){
        String[] headerRecord = {
            "Id",
            "CreatedDate",
            "AccountId",
            "AccountName",
            "AccountMarketingSegment",
            "AccountInvestmentObjectives",
            "AccountServiceModel",
            "AccountOwnerName",
            "Name",
            "AchievedPercentage",
            "AchievedPercentageRange",
            "ActualValue",
            "TargetValue",
            "TargetDate",
            "Type",
            "YearsUntilTarget"
        };
        
        return headerRecord;
    }

    public String[] getRowOfData(){
        String[] dataRecord = {
            this.getId(),
            this.getCreatedDate(),
            this.getAccountId(),
            this.getAccountName(),
            this.getAccountMarketingSegment(),
            this.getAccountInvestmentObjectives(),
            this.getAccountServiceModel(),
            this.getAccountOwnerName(),
            this.getName(),
            this.getAchievedPercentage() + "",
            this.getAchievedPercentageRange(),
            this.getActualValue() + "",
            this.getTargetValue() + "",
            this.getTargetDate(),
            this.getType(),
            this.getYearsUntilTarget() + ""
        };
        
        return dataRecord;
    }
}