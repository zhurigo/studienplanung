Layered architecture representation for better understanding our system and how the call flow works. It can be seen, in a simplified manner, as an onion with 3 layers:

- outer layer is what exposes our system to the world
- middle layer is where data is treated and served up or down, depending on the direction the data is travelling
- inner layer is what gives access to the data

Template shape of layered architecture in SWE:

```mermaid
flowchart TB
    subgraph App[Application]
        P["Presentation layer<br/>UI, controllers, API endpoints"]
        B["Business logic layer<br/>Rules, workflows, services"]
        D["Data access layer<br/>Repositories, ORM, queries"]
    end
    DB[("Database<br/>Persistent storage")]

    P -->|calls| B
    B -->|calls| D
    D -->|queries| DB
```

Layered architecture representation of studienplanung:

```mermaid
flowchart TB
    user(["Student at the terminal"])

    subgraph app["studienplanung"]
        subgraph exposed["Exposed layer: routes and handlers"]
            direction LR
            main["main.py<br/>menu loop = router"]
            display["display.py<br/>1 degree plan<br/>2 explore specialisations"]
            choices["choices.py<br/>3 choose specialisation<br/>4 plan electives"]
            rulesui["rules.py<br/>5 show_plan_check<br/>6 show_roadmap"]
            prompts["prompts.py, styling.py<br/>input, output and layout helpers"]
        end

        subgraph middle["Middle layer: business rules"]
            direction LR
            models["models.py<br/>StudentPlan<br/>choose_specialisation<br/>add_elective, remove_elective<br/>fill_missing_semesters"]
            rules["rules.py<br/>check_plan<br/>roadmap_total"]
            service["plan_service.py<br/>load_catalogue, load_saved_plan<br/>save_current_plan<br/>electives_by_category"]
        end

        subgraph persistence["Persistence layer: repositories"]
            direction LR
            loader["data_loader.py<br/>load_all (read only)"]
            storage["storage.py<br/>save_plan, load_plan"]
        end
    end

    subgraph files["Data: JSON files"]
        direction LR
        catalogue[("data/modules.json<br/>data/specialisations.json<br/>data/electives.json")]
        myplan[("my_plan.json")]
    end

    user -->|"types a menu number"| main
    main --> display
    main --> choices
    main --> rulesui
    display & choices & rulesui -.-> prompts
    choices --> models
    rulesui --> rules
    main -->|"app start, 4 electives, 7 save, 0 quit"| service
    service -->|"fill_missing_semesters"| models
    service --> loader
    service --> storage
    loader -->|"reads"| catalogue
    storage -->|"reads and writes"| myplan
```
