using UnityEngine;
using UnityEngine.UI;

public class CraftAnimationController : MonoBehaviour
{
    [Header("动画步骤")]
    public GameObject[] craftSteps;   
    public Text stepDescription;      
    public int totalSteps = 5;        

    private int currentStep;

    void Start()
    {
        currentStep = 0;
        
        foreach (var step in craftSteps)
        {
            step.SetActive(false);
        }
    }

    public void PlayCraftSteps()
    {
        currentStep = 0;
        InvokeRepeating(nameof(ShowNextStep), 0f, 3f); 
    }

    void ShowNextStep()
    {
        if (currentStep > 0)
        {
            craftSteps[currentStep - 1].SetActive(false);
        }

        if (currentStep < totalSteps)
        {
            craftSteps[currentStep].SetActive(true);
            UpdateStepDescription(currentStep);
            currentStep++;
        }
        else
        {
            CancelInvoke();
        }
    }

}
