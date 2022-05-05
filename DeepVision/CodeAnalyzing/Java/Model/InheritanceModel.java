/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package Model;

/**
 *
 * @author Roshan Withanage
 */
public class InheritanceModel {

    private int count;
    private String className;
    private int No_of_direct_inheritances;
    private int No_of_indirect_inheritances;
    private int Total_inheritances;
    private int Ci;

    public InheritanceModel() {
    }

    public InheritanceModel(int count, String className, int No_of_direct_inheritances, int No_of_indirect_inheritances, int Total_inheritances, int Ci) {
        this.count = count;
        this.className = className;
        this.No_of_direct_inheritances = No_of_direct_inheritances;
        this.No_of_indirect_inheritances = No_of_indirect_inheritances;
        this.Total_inheritances = Total_inheritances;
        this.Ci = Ci;
    }

    public int getCount() {
        return count;
    }

    public void setCount(int count) {
        this.count = count;
    }

    public String getClassName() {
        return className;
    }

    public void setClassName(String className) {
        this.className = className;
    }

    public int getNo_of_direct_inheritances() {
        return No_of_direct_inheritances;
    }

    public void setNo_of_direct_inheritances(int No_of_direct_inheritances) {
        this.No_of_direct_inheritances = No_of_direct_inheritances;
    }

    public int getNo_of_indirect_inheritances() {
        return No_of_indirect_inheritances;
    }

    public void setNo_of_indirect_inheritances(int No_of_indirect_inheritances) {
        this.No_of_indirect_inheritances = No_of_indirect_inheritances;
    }

    public int getTotal_inheritances() {
        return Total_inheritances;
    }

    public void setTotal_inheritances(int Total_inheritances) {
        this.Total_inheritances = Total_inheritances;
    }

    public int getCi() {
        return Ci;
    }

    public void setCi(int Ci) {
        this.Ci = Ci;
    }

    

}
