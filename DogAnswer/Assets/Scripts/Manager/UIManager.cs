using System.Collections.Generic;
using System.Collections;
using UnityEngine;
using UnityEngine.UI;

namespace DogAnswer
{
    public class UIManager: Utility.Singleton<UIManager>
    {
        [SerializeField]
        private GameObject ImagePrefab;
        [SerializeField]
        private Transform Container;
        [SerializeField]
        private GameObject ResultPanel;

        [SerializeField]
        private Text AlertMessage;
        [SerializeField]
        private float alphaDiff = 0.05f;
        [SerializeField]
        private string ImageBaseDirName = "DogImages/";

        public void Close(GameObject target)
        {
            target.SetActive(false);
        }

        public void Alert(string message)
        {
            StopAllCoroutines();
            StartCoroutine(FadeAlertMessage(message));
        }

        private IEnumerator FadeAlertMessage(string message)
        {
            AlertMessage.text = message;
            AlertMessage.gameObject.SetActive(true);

            for (int i = 1; i <= 20; i++)
            {
                Color originColor = AlertMessage.color;
                Color color = new Color(originColor.r, originColor.g, originColor.b, 1 - alphaDiff * i);

                AlertMessage.color = color;

                yield return new WaitForSeconds(0.1f);
            }

            AlertMessage.gameObject.SetActive(false);

            yield return null;
        }

        public void ShowImages(string dogName, List<string> imageNames)
        {
            string basePath = ImageBaseDirName + dogName;

            foreach(var imageName in imageNames)
            {
                string path = string.Format("{0}/{1}", basePath, imageName);
                Image image = Instantiate(ImagePrefab, Container).GetComponent<Image>();

                image.sprite = Resources.Load<Sprite>(path);
            }

            ResultPanel.SetActive(true);
        }
    }
}