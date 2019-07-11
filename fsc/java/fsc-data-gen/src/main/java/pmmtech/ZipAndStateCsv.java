package pmmtech;

import com.opencsv.bean.CsvBindByName;

/**
 * ZipAndStateCsv
 */
public class ZipAndStateCsv {

    @CsvBindByName(column = "ZipCode")
    private String zipCode;

    @CsvBindByName(column = "State")
    private String state;

    @CsvBindByName(column = "City")
    private String city;

    public String getZipCode() {
        return this.zipCode;
    }

    public void setZipCode(String zipCode) {
        this.zipCode = zipCode;
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
    
}