export interface CarPhoto {
  id: number;
  url: string;
  urlMachine: string;
}

export interface CarData {
  car_make: string;
  car_release_date: string;
  model: string;
  photo: CarPhoto[];
  vin: string;
}

export interface PersonData {
  LAST_NAME: string;
  NAME: string;
  SECOND_NAME: string;
}

export interface StageInfo {
  color: string;
  id: string;
  name: string;
}

export interface TrackingStage {
  color: string;
  completed: boolean;
  current: boolean;
  name: string;
  status_id: string;
}

export interface TrackingGroup {
  completed: boolean;
  current: boolean;
  description: string;
  stages: TrackingStage[];
}

export interface TrackingInfo {
  [key: string]: TrackingGroup;
}

export interface CarResponse {
  car_data: CarData;
  person_data: PersonData;
  stage_info: StageInfo;
  tracking_info: TrackingInfo;
  message: string;
  status_code: number;
}

export interface CarState {
  data: CarResponse | null;
  loading: boolean;
  error: string | null;
}