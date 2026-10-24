using UnityEngine;

public class MarketSpaceLayout : MonoBehaviour
{
    [Header("5类非遗摊位空间点位")]
    public Transform ceramicsStall;
    public Transform sugarArtStall;
    public Transform shadowPuppetryStall;
    public Transform paperCuttingStall;
    public Transform tieDyeingStall;

    [Header("游览动线设置")]
    public Transform[] tourRoutePoints;  
    public float triggerZoneRadius = 3f; 
    [Header("空间叙事节奏")]
    public float stayDurationPerStall = 45f; 

    private GameObject[] stallTriggerZones;

    void Start()
    {
        InitStallTriggerZones();
        InitTourRoute();
    }

    void InitStallTriggerZones()
    {
        Transform[] allStalls = { ceramicsStall, sugarArtStall, shadowPuppetryStall, paperCuttingStall, tieDyeingStall };
        stallTriggerZones = new GameObject[allStalls.Length];

        for (int i = 0; i < allStalls.Length; i++)
        {
            
            GameObject zone = new GameObject($"TriggerZone_{i}");
            zone.transform.SetParent(allStalls[i]);
            zone.transform.localPosition = Vector3.zero;
            
            SphereCollider collider = zone.AddComponent<SphereCollider>();
            collider.isTrigger = true;
            collider.radius = triggerZoneRadius;

            stallTriggerZones[i] = zone;
        }
    }

    void InitTourRoute()
    {
       
        int[] routeOrder = { 1, 3, 4, 0, 2 };
        Debug.Log("已加载非遗市集推荐游览动线，共5个核心体验节点");
    }

    public Transform GetStallPosition(int stallIndex)
    {
        Transform[] allStalls = { ceramicsStall, sugarArtStall, shadowPuppetryStall, paperCuttingStall, tieDyeingStall };
        if (stallIndex >= 0 && stallIndex < allStalls.Length)
        {
            return allStalls[stallIndex];
        }
        return null;
    }
}
