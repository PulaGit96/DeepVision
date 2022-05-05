/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package Controller;

import FileReader.FReader;
import Model.ControlStractureStepModel;
import Model.ControlStructuresModel;
import Model.CsNode;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 *
 * @author Roshan Withanage
 */
public class ControlStructuresController {

    private ControlStructuresController() {
    }
    private static final ControlStructuresController obj = new ControlStructuresController();

    public static ControlStructuresController getInstance() {
        return obj;
    }

    List<ControlStructuresModel> finalcsList = new ArrayList<>();
    List<ControlStructuresModel> csList = new ArrayList<>();
    List<ControlStractureStepModel> csStepList = new ArrayList<>();
    List<List<String>> methodList = new ArrayList<>();

    private int lineNo;
    private String programStatement;
    private int Wtcs;
    private int NC;
    private int Ccspps;
    private int Ccs;

    private int counter = 0;

    private int ifelseif = 2;
    private int forwhiledowhile = 3;
    private int switchswitchcase = 2;
    private int caseswitchcase = 1;

    //REGEX PATTERNS
    private final String CONTROL_STRUCTURE_IF_ELSEIF = "\\s?if\\s?\\(|\\selse if\\s?\\(";
    private final String CONTROL_STRUCTURE_FOR_WHILE_DOWHILE = "\\s?for\\s?\\(|\\s?while\\s?\\(";
    private final String CONTROL_STRUCTURE_FOR_SWITCH = "\\sswitch\\s?\\(";
    private final String CONTROL_STRUCTURE_FOR_CASE = "case\\s\\w\\s?:";
    private final String CONTROL_STRUCTURE_LOGIC_GATE = "\\|\\||&&";
    private final String CONTROL_STRUCTURE_C_METHOD = "(public|protected|private|static)\\s?:\\s?\\w*\\s\\w*";
    private final String CONTROL_STRUCTURE_JAVA_METHOD = "(public|protected|private|static|\\s) +[\\w\\<\\>\\[\\]]+\\s+(\\w+) *\\([^\\)]*\\) *(\\{?|[^;])";

    private void reset() {
        programStatement = "";
        Wtcs = 0;
        NC = 0;
        Ccspps = 0;
        Ccs = 0;
    }

    public int[] getWeights() {
        int weights[] = {ifelseif, forwhiledowhile, switchswitchcase, caseswitchcase};
        return weights;
    }

    public void setWeights(int ifelseif, int forwhiledowhile, int switchswitchcase, int caseswitchcase) {
        this.ifelseif = ifelseif;
        this.forwhiledowhile = forwhiledowhile;
        this.switchswitchcase = switchswitchcase;
        this.caseswitchcase = caseswitchcase;
    }

    public List<ControlStructuresModel> getComplexity(String filePath) {
        finalcsList.removeAll(finalcsList);
        lineNo = 0;

        MainFunction(filePath);
        List<String> LineList = FReader.getInstance().getLineList(filePath);
        for (String line : LineList) {

            for (int i = 0; i < csList.size(); i++) {
                if (csList.get(i).getProgramStatement().equals(line)) {
                    Wtcs = csList.get(i).getWtcs();
                    NC = csList.get(i).getNC();
                    Ccspps = csList.get(i).getCcspps();
                    Ccs = csList.get(i).getCcs();
                }
            }
            lineNo++;
            programStatement = line;
            ControlStructuresModel obj = new ControlStructuresModel(lineNo, programStatement, Wtcs, NC, Ccspps, Ccs);
            finalcsList.add(obj);

            reset();
        }
        return finalcsList;
    }

    private int getSteps(List<String> LineList) {
        int steps = 0;
        for (String line : LineList) {
            for (char c : line.toCharArray()) {
                if (c == '{') {
                    steps++;
                }
            }
        }
        return steps;
    }

    private void MainFunction(String filePath) {

        csList.removeAll(csList);
        csStepList.removeAll(csStepList);

        List<List<String>> resultMethodList = loadMethodList(filePath);

        for (int k = 0; k < resultMethodList.size(); k++) {

            int steps = getSteps(resultMethodList.get(k));

            for (int i = steps; i > 0; i--) {
                for (String line : resultMethodList.get(k)) {
                    for (char c : line.toCharArray()) {
                        if (c == '}') {
                            counter--;
                        }
                    }

                    if (counter == i) {
//                        System.out.println(line + "   count   " + counter + "   method  " + k);
                        //if else if
                        Pattern ifPattern = Pattern.compile(CONTROL_STRUCTURE_IF_ELSEIF);
                        Matcher ifeMatcher = ifPattern.matcher(line);
                        while (ifeMatcher.find()) {
                            Wtcs = ifelseif;
                            Pattern LogicGatePattern = Pattern.compile(CONTROL_STRUCTURE_LOGIC_GATE);
                            Matcher LogicGate = LogicGatePattern.matcher(line);
                            while (LogicGate.find()) {
                                NC++;
                            }
                            NC++;
                        }
                        //for while do-while
                        Pattern forPattern = Pattern.compile(CONTROL_STRUCTURE_FOR_WHILE_DOWHILE);
                        Matcher forMatcher = forPattern.matcher(line);
                        while (forMatcher.find()) {
                            Wtcs = forwhiledowhile;
                            Pattern LogicGatePattern = Pattern.compile(CONTROL_STRUCTURE_LOGIC_GATE);
                            Matcher LogicGate = LogicGatePattern.matcher(line);
                            while (LogicGate.find()) {
                                NC++;
                            }
                            NC++;
                        }
                        //switch
                        Pattern switchPattern = Pattern.compile(CONTROL_STRUCTURE_FOR_SWITCH);
                        Matcher switchMatcher = switchPattern.matcher(line);
                        while (switchMatcher.find()) {
                            Wtcs = switchswitchcase;
                            Pattern LogicGatePattern = Pattern.compile(CONTROL_STRUCTURE_LOGIC_GATE);
                            Matcher LogicGate = LogicGatePattern.matcher(line);
                            while (LogicGate.find()) {
                                NC++;
                            }
                            NC++;
                        }
                        //case
                        Pattern casePattern = Pattern.compile(CONTROL_STRUCTURE_FOR_CASE);
                        Matcher caseMatcher = casePattern.matcher(line);
                        while (caseMatcher.find()) {
                            Wtcs = caseswitchcase;
                            Pattern LogicGatePattern = Pattern.compile(CONTROL_STRUCTURE_LOGIC_GATE);
                            Matcher LogicGate = LogicGatePattern.matcher(line);
                            while (LogicGate.find()) {
                                NC++;
                            }
                            NC++;
                        }

                        programStatement = line;
                        Ccs = (Wtcs * NC) + Ccspps;

                        if (Ccs != 0) {
//                            System.out.println(line + "  " + Ccspps);
                            ControlStructuresModel obj = new ControlStructuresModel(0, programStatement, Wtcs, NC, Ccspps, Ccs);
                            ControlStractureStepModel objstep = new ControlStractureStepModel(0, programStatement, Wtcs, NC, Ccspps, Ccs, counter, k);
                            csList.add(obj);
                            csStepList.add(objstep);
                        }

                        reset();
                    }

                    for (char c : line.toCharArray()) {
                        if (c == '{') {
                            counter++;
                        }
                    }

                }
                counter = 0;
            }

        }
        for (int i = csStepList.size() - 1; i > 0; i--) {
            int j = i - 1;
            if (j >= 0) {
                if (csStepList.get(j).getMethod() == csStepList.get(i).getMethod()) {
                    if (csStepList.get(j).getStep() == csStepList.get(i).getStep()) {
                        csList.get(j).setCcspps(csList.get(i).getCcspps());
                        csList.get(j).setCcs(csList.get(j).getCcs() + csList.get(i).getCcspps());
                    } else {

                        csList.get(j).setCcspps(csList.get(i).getCcs());
                        csList.get(j).setCcs(csList.get(j).getCcs() + csList.get(i).getCcs());
                    }
                }
            }
        }
    }

    private List<List<String>> loadMethodList(String filePath) {
        System.out.println("called");
        methodList.removeAll(methodList);

        List<String> LineList = FReader.getInstance().getLineList(filePath);
        int count = 0;
        String found = "Not Found";
        for (String line : LineList) {

            //methods
            Pattern methodPattern = Pattern.compile(CONTROL_STRUCTURE_JAVA_METHOD);
            Matcher methodMatcher = methodPattern.matcher(line);
            while (methodMatcher.find()) {
                found = "Found";
                count = 0;
                CsNode.getInstance().createNode();
            }
            Pattern methodcPattern = Pattern.compile(CONTROL_STRUCTURE_C_METHOD);
            Matcher methodcMatcher = methodcPattern.matcher(line);
            while (methodcMatcher.find()) {
                found = "Found";
                count = 0;
                CsNode.getInstance().createNode();
            }

            for (char c : line.toCharArray()) {
                if (c == '{') {
                    count++;
                }
            }

            if (found.equals("Found") && count > 0) {
                CsNode.getInstance().addLine(line);
            }
            for (char c : line.toCharArray()) {
                if (c == '}') {
                    count--;
                }
            }
            if (found.equals("Found") && count == 0) {
                methodList.add(CsNode.getInstance().getCsNode());
            }

            if (count == 0) {
                found = "Not Found";
            }

        }

//        for (int i = 0; i < methodList.size(); i++) {
////            System.out.println(methodList.get(i));
//            for (int j = 0; j < methodList.get(i).size(); j++) {
//                System.out.println(methodList.get(i).get(j));
//            }
//        }
        return methodList;
    }

}
