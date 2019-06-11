package pmmtech;

import com.opencsv.bean.CsvBindByName;

/**
 * LeadCsv
 */
public class LeadCsv {

    @CsvBindByName(column = "Id")
    private String id;
    
    @CsvBindByName(column = "CreatedDate")
    private String createdDate;

    @CsvBindByName(column = "Status")
    private String status;

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

}