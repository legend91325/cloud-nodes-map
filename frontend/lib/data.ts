import axios from 'axios';
import { CloudNode, ProviderMetadata } from '@/types';

const PROVIDER_IDS = [
  'alibaba-cloud',
  'aws',
  'azure',
  'google-cloud',
  'huawei-cloud',
  'tencent-cloud',
  'volcano-engine',
  'oracle-cloud',
  'ibm-cloud',
  'ovh-cloud',
  'digitalocean',
];

const PROVIDER_MAP: Record<string, string> = {
  'alibaba-cloud': 'alibaba_cloud',
  'aws': 'aws',
  'azure': 'azure',
  'google-cloud': 'google_cloud',
  'huawei-cloud': 'huawei_cloud',
  'tencent-cloud': 'tencent_cloud',
  'volcano-engine': 'volcano_engine',
  'oracle-cloud': 'oracle_cloud',
  'ibm-cloud': 'ibm_cloud',
  'ovh-cloud': 'ovh_cloud',
  'digitalocean': 'digitalocean',
};

export async function loadAllNodes(): Promise<CloudNode[]> {
  try {
    const promises = PROVIDER_IDS.map(async (providerId) => {
      const response = await axios.get(`/data/${providerId}/nodes.json`);
      const data = response.data;
      const providerKey = PROVIDER_MAP[providerId];
      
      return data.nodes.map((node: any) => ({
        ...node,
        provider: providerKey,
      }));
    });

    const results = await Promise.all(promises);
    return results.flat();
  } catch (error) {
    console.error('Failed to load nodes:', error);
    return [];
  }
}

export async function loadProviderMetadata(): Promise<ProviderMetadata | null> {
  try {
    const response = await axios.get('/data/providers-metadata.json');
    return response.data;
  } catch (error) {
    console.error('Failed to load provider metadata:', error);
    return null;
  }
}

export function getAvailabilityZoneCount(node: CloudNode): number {
  if (node.availability_zones) {
    if (Array.isArray(node.availability_zones)) {
      return node.availability_zones.length;
    } else if (typeof node.availability_zones === 'number') {
      return node.availability_zones;
    }
  } else if (node.availability_zone) {
    return 1;
  }
  return 0;
}

