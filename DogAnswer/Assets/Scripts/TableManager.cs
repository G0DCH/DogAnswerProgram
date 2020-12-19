using System.Collections.Generic;
using System.Collections;
using UnityEngine;

namespace DogAnswer
{
    public class TableManager: MonoBehaviour
    {
        public string TableName = "VectorTable";
        public VectorTable vectorTable;

        private void Start()
        {
            var fileData = CSVReader.Read(TableName);
            vectorTable = fileData;

            Debug.Log(fileData.Columns);
        }
    }
}