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
public class SummaryModel {

    private int line_no;
    private String program_Statement;
    private int Ci;
    private int Ccs;
    private int TCps;

    public SummaryModel() {
    }

    public SummaryModel(int line_no, String program_Statement, int Ci, int Ccs, int TCps) {
        this.line_no = line_no;
        this.program_Statement = program_Statement;
        this.Ci = Ci;
        this.Ccs = Ccs;
        this.TCps = TCps;
    }

    public int getLine_no() {
        return line_no;
    }

    public void setLine_no(int line_no) {
        this.line_no = line_no;
    }

    public String getProgram_Statement() {
        return program_Statement;
    }

    public void setProgram_Statement(String program_Statement) {
        this.program_Statement = program_Statement;
    }

    public int getCi() {
        return Ci;
    }

    public void setCi(int Ci) {
        this.Ci = Ci;
    }

    public int getCcs() {
        return Ccs;
    }

    public void setCcs(int Ccs) {
        this.Ccs = Ccs;
    }

    public int getTCps() {
        return TCps;
    }

    public void setTCps(int TCps) {
        this.TCps = TCps;
    }

}
