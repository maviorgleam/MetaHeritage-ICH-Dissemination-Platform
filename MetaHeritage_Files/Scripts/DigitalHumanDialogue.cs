using UnityEngine;

public class DigitalHumanDialogue : MonoBehaviour
{
    [Header("对话设置")]
    public AudioClip greetingAudio;    
    public GameObject dialogueUI;      
    public bool isQaModeEnabled;     

    private AudioSource audioSource;
    private bool hasGreeted;

    void Start()
    {
        audioSource = GetComponent<AudioSource>();
        dialogueUI.SetActive(false);
        hasGreeted = false;
    }

    void OnTriggerEnter(Collider other)
    {
        if (other.CompareTag("Player") && !hasGreeted)
        {
            hasGreeted = true;
            audioSource.clip = greetingAudio;
            audioSource.Play();
            dialogueUI.SetActive(true);
        }
    }

    public void StartQAMode()
    {
        if (isQaModeEnabled)
        {
            Debug.Log("启动非遗知识自由问答模式");
        }
    }

    void OnTriggerExit(Collider other)
    {
        if (other.CompareTag("Player"))
        {
            dialogueUI.SetActive(false);
            audioSource.Stop();
            hasGreeted = false;
        }
    }
}
