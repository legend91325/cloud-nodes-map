export interface CloudNode {
  node_id: string;
  name: string;
  provider: string;
  location: {
    continent: string;
    country: string;
    city: string;
    latitude: number;
    longitude: number;
  };
  availability_zones?: string[] | number;
  availability_zone?: string;
  status: 'active' | 'inactive';
  launch_date?: string;
  data_center?: string;
  network_info: {
    latency: number;
    uptime: number;
  };
}

export interface Provider {
  id: string;
  name: string;
  name_en: string;
  color: string;
  founded: string;
  headquarters: string;
  data_path: string;
  website: string;
  description: string;
  market_position: string;
}

export interface ProviderMetadata {
  version: string;
  last_updated: string;
  providers: Record<string, Provider>;
  color_scheme: {
    description: string;
    palette: Array<{
      provider: string;
      color: string;
      rgb: number[];
    }>;
  };
  statistics: {
    total_providers: number;
    total_regions: number;
    last_calculation: string;
  };
}

export interface CountryStat {
  country: string;
  continent: string;
  providers: string[];
  nodeCount: number;
  azCount: number;
}

export interface ProviderStat {
  provider: string;
  name: string;
  color: string;
  nodeCount: number;
  countryCount: number;
  azCount: number;
}

