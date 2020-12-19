using System.Collections.Generic;
using System.Collections;
using UnityEngine;
using UnityEngine.UI;

namespace DogAnswer
{
    public class UIManager: Utility.Singleton<UIManager>
    {
        [SerializeField]
        private Text AlertMessage;

        [SerializeField]
        private float alphaDiff = 0.1f;

        public void Close(GameObject target)
        {
            target.SetActive(false);
        }

        public void Alert(string message)
        {
            StartCoroutine(FadeAlertMessage(message));
        }

        private IEnumerator FadeAlertMessage(string message)
        {
            AlertMessage.text = message;
            AlertMessage.gameObject.SetActive(true);

            for (int i = 1; i <= 10; i++)
            {
                Color originColor = AlertMessage.color;
                Color color = new Color(originColor.r, originColor.g, originColor.b, 1 - alphaDiff * i);

                AlertMessage.color = color;

                yield return new WaitForSeconds(0.2f);
            }

            AlertMessage.gameObject.SetActive(false);

            yield return null;
        }
    }
}