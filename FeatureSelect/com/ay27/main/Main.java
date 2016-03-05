package com.ay27.main;

import java.io.*;

import weka.attributeSelection.AttributeSelection;
import weka.attributeSelection.BestFirst;
import weka.attributeSelection.CfsSubsetEval;
import weka.core.Instances;
import weka.core.converters.ArffLoader;

public class Main {

    private ArffLoader loader;
    private Instances dataSet;
    private File arffFile;
    private int sizeOfDataset;
    private int numOfOldAttributes;
    private int numOfNewAttributes;
    private int classIndex;
    private int[] selectedAttributes;

    public Main(File file) throws IOException {
        loader = new ArffLoader();
        arffFile = file;
        loader.setFile(arffFile);
        dataSet = loader.getDataSet();
        sizeOfDataset = dataSet.numInstances();
        numOfOldAttributes = dataSet.numAttributes();
        classIndex = numOfOldAttributes - 1;
        dataSet.setClassIndex(classIndex);
    }

    public void select() throws Exception {
        CfsSubsetEval evaluator = new CfsSubsetEval();
        BestFirst search = new BestFirst();
        AttributeSelection eval = new AttributeSelection();

        eval.setEvaluator(evaluator);
        eval.setSearch(search);

        eval.SelectAttributes(dataSet);
        numOfNewAttributes = eval.numberAttributesSelected();
        selectedAttributes = eval.selectedAttributes();

        for (int i = 0; i < selectedAttributes.length - 1; i++) {
            System.out.print(" " + selectedAttributes[i]);
        }
    }

    /**
     * Use:
     * FeatureSelect.jar [file name]
     */
    public static void main(String[] args) {
        File file = new File(args[0]);
        try {
            Main ws = new Main(file);
            ws.select();

        } catch (Exception e) {
            e.printStackTrace();
        }

    }

}
