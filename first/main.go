package main

import (
    "database/sql"
    "fmt"
    "log"
    "time"

    _ "github.com/lib/pq"
)

func main() {
    connStr := "user=postgres dbname=mydb password=postgres host=localhost port=5000 sslmode=disable"
    db, err := sql.Open("postgres", connStr)
    if err != nil {
        log.Fatal(err)
    }
    defer db.Close()

    for i := 0; ; i++ {
        _, err = db.Exec(`INSERT INTO mytable (name, email) VALUES ($1, $2)`, fmt.Sprintf("John Doe %d", i), fmt.Sprintf("john%d@example.com", i))
        if err != nil {
            log.Fatal(err)
        }

        rows, err := db.Query("SELECT * FROM mytable")
        if err != nil {
            log.Fatal(err)
        }

        for rows.Next() {
            var id int
            var name string
            var email string
            err = rows.Scan(&id, &name, &email)
            if err != nil {
                log.Fatal(err)
            }
            fmt.Println(id, name, email)
        }

        if err = rows.Err(); err != nil {
            log.Fatal(err)
        }

        rows.Close()

        time.Sleep(1 * time.Second)
    }
}