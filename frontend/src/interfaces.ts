export interface IStatus {
    index: string
    statusName: string
    information: string
    date: string
    is_active: boolean
}

export interface ICar {
    name: string
    VIN: string
    photos: string[]
    year_release: string
}