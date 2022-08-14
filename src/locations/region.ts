import District from "./district";

export default class Region {
    public readonly id: string;
    public readonly name: string;

    public readonly districts: District[] = []

    constructor(id: string, name: string, districts: District[]) {
        this.id = id;
        this.name = name;

        this.districts = districts;
    }
}