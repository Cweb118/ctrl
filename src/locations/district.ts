export default class District {
    public readonly id: string;
    public readonly name: string;

    public readonly paths: District[] = [];

    constructor(id: string, name: string) {
        this.id = id;
        this.name= name;
    }
}