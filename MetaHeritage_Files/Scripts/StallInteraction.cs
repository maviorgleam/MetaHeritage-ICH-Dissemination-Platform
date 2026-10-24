using UnityEngine;

public class StallInteraction : MonoBehaviour
{
    [Header("交互设置")]
    public string stallName;          
    public GameObject introPanel;    
    public AudioClip narrationAudio;  
    public GameObject craftAnimation; 

    private AudioSource audioSource;
    private bool isPlayerInRange;

    void Start()
    {
        audioSource = GetComponent<AudioSource>();
        introPanel.SetActive(false);
        craftAnimation.SetActive(false);
    }


    void OnTriggerEnter(Collider other)
    {
        if (other.CompareTag("Player"))
        {
            isPlayerInRange = true;
            introPanel.SetActive(true);
            
            if (narrationAudio != null)
            {
                audioSource.clip = narrationAudio;
                audioSource.Play();
            }
        }
    }

    
    void OnTriggerExit(Collider other)
    {
        if (other.CompareTag("Player"))
        {
            isPlayerInRange = false;
            introPanel.SetActive(false);
            craftAnimation.SetActive(false);
            audioSource.Stop();
        }
    }

    
    void OnMouseDown()
    {
        if (isPlayerInRange)
        {
            craftAnimation.SetActive(true);
            craftAnimation.GetComponent<CraftAnimationController>().PlayCraftSteps();
        }
    }
}
