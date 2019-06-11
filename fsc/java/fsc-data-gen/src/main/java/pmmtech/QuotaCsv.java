package pmmtech;

import com.opencsv.bean.CsvBindByName;

/**
 * QuotaCsv
 */
public class QuotaCsv {

    @CsvBindByName(column = "User")
    private String user;

    @CsvBindByName(column = "State")
    private String state;

    @CsvBindByName(column = "City")
    private String city;

    @CsvBindByName(column = "StartDate")
    private String startDate;

    @CsvBindByName(column = "QuotaAmount")
    private int quotaAmount;

    public void setUserOwnerData(UserOwnerCsv userOwner){
        this.setUser(userOwner.getName());
        this.setCity(userOwner.getCity());
        this.setState(userOwner.getState());
    }

    public String getUser() {
        return this.user;
    }

    public void setUser(String user) {
        this.user = user;
    }

    public String getState() {
        return this.state;
    }

    public void setState(String state) {
        this.state = state;
    }

    public String getCity() {
        return this.city;
    }

    public void setCity(String city) {
        this.city = city;
    }

    public String getStartDate() {
        return this.startDate;
    }

    public void setStartDate(String startDate) {
        this.startDate = startDate;
    }

    public int getQuotaAmount() {
        return this.quotaAmount;
    }

    public void setQuotaAmount(int quotaAmount) {
        this.quotaAmount = quotaAmount;
    }

}