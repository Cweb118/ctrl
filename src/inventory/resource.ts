export default class Resource {
    public readonly id: string;
    public readonly name: string;

    constructor(id: string, name: string) {
        this.id = id;
        this.name = name;
    }
}

export const water = new Resource('water', 'Water')
export const food = new Resource('food', 'Food')