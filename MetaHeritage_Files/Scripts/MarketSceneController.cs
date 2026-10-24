using UnityEngine;

public class MarketSceneController : MonoBehaviour
{
    [Header("摊位交互点位")]
    public GameObject[] stallPoints;  
    public int totalStalls = 5;

    [Header("场景设置")]
    public float walkSpeed = 3.5f;
    public bool enableAutoGuide = false; 

    void Start()
    {
        
        foreach (var stall in stallPoints)
        {
            stall.GetComponent<StallInteraction>().enabled = true;
        }
    }


    public void ToggleAutoGuide()
    {
        enableAutoGuide = !enableAutoGuide;
        Debug.Log($"自动导览模式：{(enableAutoGuide ? "开启" : "关闭")}");
    }

    public Transform GetStallPosition(int stallIndex)
    {
        if (stallIndex >= 0 && stallIndex < totalStalls)
        {
            return stallPoints[stallIndex].transform;
        }
        return null;
    }
}
