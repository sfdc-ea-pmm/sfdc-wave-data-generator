package pmmtech;

import com.opencsv.bean.CsvBindByName;

/**
 * LeadCsv
 */
public class LeadCsv {

    @CsvBindByName(column = "Id", required = false)
    private String id;

    @CsvBindByName(column = "CreatedDate")
    private String createdDate;

    @CsvBindByName(column = "ConvertedDate")
    private String convertedDate;

    @CsvBindByName(column = "LastActivityDate", required = false)
    private String lastActivityDate;

    @CsvBindByName(column = "LastModifiedDate", required = false)
    private String lastModifiedDate;

    @CsvBindByName(column = "Status")
    private String status;

    @CsvBindByName(column = "LeadAge", required = false)
    private long leadAge;

    @CsvBindByName(column = "AgeGroup", required = false)
    private String ageGroup;

    @CsvBindByName(column = "LeadSource")
    private String leadSource;

    @CsvBindByName(column = "FirstName")
    private String firstName;

    @CsvBindByName(column = "LastName")
    private String lastName;

    @CsvBindByName(column = "Name", required = false)
    private String name;

    @CsvBindByName(column = "ActivityTouches", required = false)
    private int activityTouches;

    @CsvBindByName(column = "ActivityTouchesToConvert", required = false)
    private int activityTouchesToConvert;

    @CsvBindByName(column = "TouchesToConvert", required = false)
    private String touchesToConvert;

    @CsvBindByName(column = "OwnerName", required = false)
    private String ownerName;

    @CsvBindByName(column = "StartState", required = false)
    private String startState;

    @CsvBindByName(column = "AnnualRevenue", required = false)
    private long annualRevenue;

    @CsvBindByName(column = "ExpressedInterest", required = false)
    private String expressedInterest;

    @CsvBindByName(column = "Email", required = false)
    private String email;

    @CsvBindByName(column = "Phone", required = false)
    private String phone;

    @CsvBindByName(column = "ReferredByUser", required = false)
    private String referredByUser;

    @CsvBindByName(column = "ReferredByContact", required = false)
    private String referredByContact;

    @CsvBindByName(column = "Referrer", required = false)
    private String referrer;

    @CsvBindByName(column = "ReferrerType", required = false)
    private String referrerType;

    @CsvBindByName(column = "RecordTypeDeveloperName", required = false)
    private String recordTypeDeveloperName;

    @CsvBindByName(column = "Rating", required = false)
    private String rating;

    @CsvBindByName(column = "DaysSinceLastActivity", required = false)
    private long daysSinceLastActivity;

    @CsvBindByName(column = "DaysSinceActivityGroup", required = false)
    private String daysSinceActivityGroup;

    @CsvBindByName(column = "PotentialValue", required = false)
    private long potentialValue;

    @CsvBindByName(column = "ValueBucket", required = false)
    private String valueBucket;

    @CsvBindByName(column = "ConvertedOppCloseDate", required = false)
    private String convertedOppCloseDate;

    @CsvBindByName(column = "OwnerId", required = false)
    private String ownerId;

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

    public String getTouchesToConvert() {
        return Integer.valueOf(this.activityTouchesToConvert).toString();
    }

    public String getConvertedDate() {
        return this.convertedDate;
    }

    public void setConvertedDate(String convertedDate) {
        this.convertedDate = convertedDate;
    }
    public void setAgeGroup(String ageGroup) {
        this.ageGroup = ageGroup;
    }

    public String getLeadSource() {
        return this.leadSource;
    }

    public void setLeadSource(String leadSource) {
        this.leadSource = leadSource;
    }

    public String getFirstName() {
        return this.firstName;
    }

    public void setFirstName(String firstName) {
        this.firstName = firstName;
    }

    public String getLastName() {
        return this.lastName;
    }

    public void setLastName(String lastName) {
        this.lastName = lastName;
    }

    public String getName() {
        return this.name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getActivityTouches() {
        return this.activityTouches;
    }

    public void setActivityTouches(int activityTouches) {
        this.activityTouches = activityTouches;
    }

    public int getActivityTouchesToConvert() {
        return this.activityTouchesToConvert;
    }

    public void setActivityTouchesToConvert(int activityTouchesToConvert) {
        this.activityTouchesToConvert = activityTouchesToConvert;
    }

    public String getProductInterest() {
        return this.productInterest;
    }

    public void setProductInterest(String productInterest) {
        this.productInterest = productInterest;
    }

    public boolean isConverted() {
        return this.converted;
    }

    public boolean getConverted() {
        return this.converted;
    }

    public void setConverted(boolean converted) {
        this.converted = converted;
    }

    @CsvBindByName(column = "ProductInterest", required = false)
    private String productInterest;

    @CsvBindByName(column = "IsConverted")
    private boolean converted;

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

    public String getStatus() {
        return this.status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public long getLeadAge() {
        return this.leadAge;
    }

    public void setLeadAge(long leadAge) {
        this.leadAge = leadAge;
    }

    public String getAgeGroup() {
        this.ageGroup = "";

        if (this.leadAge < 15) {
            this.ageGroup = "1. < 15 days";
        } 
        else if (this.leadAge < 30){
            this.ageGroup = "2. 15-30 days";
        }
        else if (this.leadAge < 60){
            this.ageGroup = "3. 30-60 days";
        }
        else if (this.leadAge < 120){
            this.ageGroup = "4. 60-120 days";
        }
        else {
            this.ageGroup = "5. More than 120 days";
        }

        return this.ageGroup;
    }	

    public String getLastActivityDate() {
        return this.lastActivityDate;
    }

    public void setLastActivityDate(String lastActivityDate) {
        this.lastActivityDate = lastActivityDate;
    }
    public void setTouchesToConvert(String touchesToConvert) {
        this.touchesToConvert = touchesToConvert;
    }

    public String getOwnerName() {
        return this.ownerName;
    }

    public void setOwnerName(String ownerName) {
        this.ownerName = ownerName;
    }

    public String getStartState() {
        return this.startState;
    }

    public void setStartState(String startState) {
        this.startState = startState;
    }

    public long getAnnualRevenue() {
        return this.annualRevenue;
    }

    public void setAnnualRevenue(long annualRevenue) {
        this.annualRevenue = annualRevenue;
    }

    public String getExpressedInterest() {
        return this.expressedInterest;
    }

    public void setExpressedInterest(String expressedInterest) {
        this.expressedInterest = expressedInterest;
    }

    public String getEmail() {
        return this.email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getPhone() {
        return this.phone;
    }

    public void setPhone(String phone) {
        this.phone = phone;
    }

    public String getReferredByUser() {
        return this.referredByUser;
    }

    public void setReferredByUser(String referredByUser) {
        this.referredByUser = referredByUser;
    }

    public String getReferredByContact() {
        return this.referredByContact;
    }

    public void setReferredByContact(String referredByContact) {
        this.referredByContact = referredByContact;
    }

    public String getReferrer() {
        return this.referrer;
    }

    public void setReferrer(String referrer) {
        this.referrer = referrer;
    }

    public String getReferrerType() {
        if (this.referredByUser != null && !this.referredByUser.equals("")) {
            this.referrerType = "Internal";
        } 
        
        if (this.referredByContact != null && !this.referredByContact.equals("")) {
            this.referrerType = "External";
        }

        return this.referrerType;
    }

    public void setReferrerType(String referrerType) {
        this.referrerType = referrerType;
    }

    public String getRecordTypeDeveloperName() {
        return this.recordTypeDeveloperName;
    }

    public void setRecordTypeDeveloperName(String recordTypeDeveloperName) {
        this.recordTypeDeveloperName = recordTypeDeveloperName;
    }

    public String getRating() {
        return this.rating;
    }

    public void setRating(String rating) {
        this.rating = rating;
    }

    public long getDaysSinceLastActivity() {
        return this.daysSinceLastActivity;
    }

    public void setDaysSinceLastActivity(long daysSinceLastActivity) {
        this.daysSinceLastActivity = daysSinceLastActivity;
    }

    public String getDaysSinceActivityGroup() {
        /*
        case when 'DaysSinceLastActivity' < 15 then \"1. < 15 days\" 
        when 'DaysSinceLastActivity' < 30 then \"2. 15-30 days\" 
        when 'DaysSinceLastActivity' < 60 then \"3. 30-60 days\" 
        when 'DaysSinceLastActivity' < 120 then \"4. 60-120 days\" 
        else \"5. More than 120 days\" end
        */

        if (this.daysSinceLastActivity <= 15) {
            this.daysSinceActivityGroup = "1. < 15 days";
        }         
        else if (this.daysSinceLastActivity >= 15 && this.daysSinceLastActivity < 30){
            this.daysSinceActivityGroup = "2. 15-30 days";
        }
        else if (this.daysSinceLastActivity >= 30 && this.daysSinceLastActivity < 60){
            this.daysSinceActivityGroup = "3. 30-60 days";
        }
        else if (this.daysSinceLastActivity >= 60 && this.daysSinceLastActivity < 120){
            this.daysSinceActivityGroup = "4. 60-120 days";
        }
        else {
            this.daysSinceActivityGroup = "5. More than 120 days";
        }

        return this.daysSinceActivityGroup;
    }

    public void setDaysSinceActivityGroup(String daysSinceActivityGroup) {
        this.daysSinceActivityGroup = daysSinceActivityGroup;
    }

    public long getPotentialValue() {
        return this.potentialValue;
    }

    public void setPotentialValue(long potentialValue) {
        this.potentialValue = potentialValue;
    }

    public String getValueBucket() {
        /*
        case when 'FinServ__PotentialValue__c' <= 100000 then \"1. < 100K\" 
        when 'FinServ__PotentialValue__c' <= 250000 then \"2. 100K - 250K\" 
        when 'FinServ__PotentialValue__c' <= 500000 then \"3. 250K - 500K\" 
        when 'FinServ__PotentialValue__c' > 500000 then \"4. More than 500K\" 
        else \"5. Not set\" end
        */

        if (this.potentialValue <= 100000) {
            this.valueBucket = "1. < 100K";
        }         
        else if (this.potentialValue > 100000 && this.potentialValue <= 250000){
            this.valueBucket = "2. 100K - 250K";
        }
        else if (this.potentialValue > 250000 && this.potentialValue <= 500000){
            this.valueBucket = "3. 250K - 500K";
        }
        else {
            this.valueBucket = "4. More than 500K";
        }

        return this.valueBucket;
    }

    public void setValueBucket(String valueBucket) {
        this.valueBucket = valueBucket;
    }

    public String getConvertedOppCloseDate() {
        return this.convertedOppCloseDate;
    }

    public void setConvertedOppCloseDate(String convertedOppCloseDate) {
        this.convertedOppCloseDate = convertedOppCloseDate;
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

    public String getLastModifiedDate() {
        return this.lastModifiedDate;
    }

    public void setLastModifiedDate(String lastModifiedDate) {
        this.lastModifiedDate = lastModifiedDate;
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