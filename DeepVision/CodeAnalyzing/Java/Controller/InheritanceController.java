/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package Controller;

import FileReader.FReader;
import Model.InheritanceModel;
import Model.Node;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 *
 * @author Roshan Withanage
 */
public class InheritanceController {

    private int count = 0;
    private String className = "";
    private int No_of_direct_inheritances = 0;
    private int No_of_indirect_inheritances = 0;
    private int Total_inheritances = 0;
    private int Ci = 0;

    private int inheritNon = 0;
    private int inheritOne = 1;
    private int inheritTwo = 2;
    private int inheritThree = 3;
    private int inheritMore = 4;

    //REGEX PATTERNS
    private final String INHERITANCE_CLASS = "\\w*\\sextends\\s\\w*";
    private final String FIND_CLASS = "class\\s\\w*";
    private final String FIND_C_ClASS = "class\\s\\w*\\s?:\\s|,";
    private final String FIND_C_ClASS_STEP = "class\\s\\w*\\s?:\\s?";

    List<Node> nodeList = new ArrayList<>();

    List<String> classList = new ArrayList<>();

    List<InheritanceModel> inheritanceModelList = new ArrayList<>();

    private InheritanceController() {
    }
    private static final InheritanceController obj = new InheritanceController();

    public static InheritanceController getInstance() {
        return obj;
    }

    private void reset() {
        className = "";
        No_of_direct_inheritances = 0;
        No_of_indirect_inheritances = 0;
        Total_inheritances = 0;
        Ci = 0;
    }

    public int[] getWeights() {
        int weights[] = {inheritNon, inheritOne, inheritTwo, inheritThree, inheritMore};
        return weights;
    }

    public void setWeights(int inheritNon, int inheritOne, int inheritTwo, int inheritThree, int inheritMore) {
        this.inheritNon = inheritNon;
        this.inheritOne = inheritOne;
        this.inheritTwo = inheritTwo;
        this.inheritThree = inheritThree;
        this.inheritMore = inheritMore;
    }

    public List<InheritanceModel> getComplexity(List<String> fileListPath, String filePath) {
        loadDatatoList(fileListPath);
        inheritanceModelList.removeAll(inheritanceModelList);
        count = 0;

        List<String> LineList = FReader.getInstance().getLineList(filePath);
        for (String line : LineList) {
            //direct inheritance
            Pattern directInheritancePattern = Pattern.compile(INHERITANCE_CLASS);
            Matcher directInheritanceMatcher = directInheritancePattern.matcher(line);
            while (directInheritanceMatcher.find()) {

                if (isUserDefindClass(directInheritanceMatcher.group().split(" ")[2])) {
                    No_of_direct_inheritances++;
                }
                //indirect inheritance
                No_of_indirect_inheritances += getIndirectInheritance(directInheritanceMatcher.group().split(" ")[2]);

            }

            //find class name
            Pattern classNamePattern = Pattern.compile(FIND_CLASS);
            Matcher classNameMatcher = classNamePattern.matcher(line);
            while (classNameMatcher.find()) {
                className = classNameMatcher.group().replaceFirst("class ", "");

                Pattern classCPattern = Pattern.compile(FIND_C_ClASS_STEP);
                Matcher classCMatcher = classCPattern.matcher(line);
                while (classCMatcher.find()) {
                    Pattern classStepPattern = Pattern.compile(FIND_C_ClASS);
                    Matcher classStepMatcher = classStepPattern.matcher(line);
                    while (classStepMatcher.find()) {
                        No_of_direct_inheritances++;

                    }

                }

            }

            Total_inheritances = No_of_direct_inheritances + No_of_indirect_inheritances;

            if (Total_inheritances == 1) {
                Ci = inheritOne;
            } else if (Total_inheritances == 2) {
                Ci = inheritTwo;
            } else if (Total_inheritances == 3) {
                Ci = inheritThree;
            } else if (Total_inheritances > 3) {
                Ci = inheritMore;
            } else {
                Ci = inheritNon;
            }

            count++;
            InheritanceModel obj = new InheritanceModel(count, className, No_of_direct_inheritances, No_of_indirect_inheritances, Total_inheritances, Ci);
            inheritanceModelList.add(obj);
            reset();
        }

        return inheritanceModelList;
    }

    private void loadDatatoList(List<String> fileListPath) {

        for (int i = 0; i < fileListPath.size(); i++) {
            List<String> LineList = FReader.getInstance().getLineList(fileListPath.get(i));
            for (String line : LineList) {

                //create node
                Pattern nodePattern = Pattern.compile(INHERITANCE_CLASS);
                Matcher nodeMatcher = nodePattern.matcher(line);
                if (nodeMatcher.find()) {
                    Node obj = new Node();
                    obj.setClassName(nodeMatcher.group().split(" ")[0]);
                    obj.setSuperClass(nodeMatcher.group().split(" ")[2]);
                    obj.setChildClass("");

                    nodeList.add(obj);
                }

                //find class name
                Pattern classNamePattern = Pattern.compile(FIND_CLASS);
                Matcher classNameMatcher = classNamePattern.matcher(line);
                if (classNameMatcher.find()) {
                    classList.add(classNameMatcher.group().replaceFirst("class ", ""));
                }
            }
        }
    }

    private boolean isUserDefindClass(String className) {

        for (int i = 0; i < classList.size(); i++) {
            if (classList.get(i).equals(className)) {
                return true;
            }
        }
        return false;
    }

    private int getIndirectInheritance(String className) {
        int indirectInheritanceLevel = 0;
        for (int i = 0; i < nodeList.size(); i++) {
            if (nodeList.get(i).getClassName().equals(className)) {
                if (isUserDefindClass(nodeList.get(i).getSuperClass())) {
                    indirectInheritanceLevel++;
                    getIndirectInheritance(nodeList.get(i).getSuperClass());
                }
            }
        }

        return indirectInheritanceLevel;
    }

}
