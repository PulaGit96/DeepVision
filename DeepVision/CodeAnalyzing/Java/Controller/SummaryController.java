/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package Controller;

import Model.ControlStructuresModel;
import Model.InheritanceModel;
import Model.SummaryModel;
import java.util.ArrayList;
import java.util.List;

/**
 *
 * @author Roshan Withanage
 */
public class SummaryController {

    private int line_no;
    private String program_Statement;
    private int Ci;
    private int Ccs;
    private int TCps;

    private SummaryController() {
    }

    private static final SummaryController obj = new SummaryController();

    List<SummaryModel> totalC = new ArrayList<SummaryModel>();

    public static SummaryController getInstance() {
        return obj;
    }

    public List<SummaryModel> getTotalComplexity(List<String> fileListPath, String filePath) {

        List<ControlStructuresModel> Ccslist = ControlStructuresController.getInstance().getComplexity(filePath);
        List<InheritanceModel> Cilist = InheritanceController.getInstance().getComplexity(fileListPath, filePath);

        for (int i = 0; i < Cilist.size(); i++) {
            line_no = Ccslist.get(i).getLineNo();
            program_Statement = Ccslist.get(i).getProgramStatement();
            Ci = Cilist.get(i).getCi();
            Ccs = Ccslist.get(i).getCcs();
//
            TCps = Ci + Ccs;
//
//            System.out.println(TCps);
//
            SummaryModel obj = new SummaryModel(line_no, program_Statement, Ci, Ccs, TCps);
            totalC.add(obj);

        }

        return totalC;
    }

}
