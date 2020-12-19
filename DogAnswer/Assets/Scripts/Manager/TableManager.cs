using System.Collections.Generic;
using System.Collections;
using UnityEngine;

namespace DogAnswer
{
    public class TableManager : Utility.Singleton<TableManager>
    {
        [SerializeField]
        private string TableName = "VectorTables";
        public Dictionary<string, VectorTable> vectorTables = new Dictionary<string, VectorTable>();
        public List<string> DogNames = new List<string>();

        private void Start()
        {
            var tableDatas = CSVReader.Read(TableName);
            foreach (var tableData in tableDatas)
            {
                vectorTables.Add(tableData.DogName, tableData);
                DogNames.Add(tableData.DogName);
            }
        }
    }
}