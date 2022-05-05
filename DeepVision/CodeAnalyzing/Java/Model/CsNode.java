/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package Model;

import java.util.ArrayList;
import java.util.List;

/**
 *
 * @author Roshan Withanage
 */
public class CsNode {

    private CsNode() {
    }
    private static final CsNode obj = new CsNode();

    public static CsNode getInstance() {
        return obj;
    }

    private List<String> CsNodeList = new ArrayList<>();

    public void createNode() {
        CsNodeList = new ArrayList<>();
    }

    public void addLine(String line) {
        CsNodeList.add(line);
    }

    public List<String> getCsNode() {
        return CsNodeList;
    }
}
