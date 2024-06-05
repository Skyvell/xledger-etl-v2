from gql import gql 


GET_TIMESHEETS = gql("""
    query getTimesheets($first: Int, $after: String, $modifiedAt_gt: DateTimeString, $modifiedAt_lte: DateTimeString) {
        timesheets(
            first: $first, 
            after: $after, 
            filter: {
                dbId_in: "",
                modifiedAt_gt: $modifiedAt_gt, 
                modifiedAt_lte: $modifiedAt_lte, 
                assignmentDate_gte: "2024-01-01", 
                assignmentDate_lte: "2024-06-01"
            }
        ) {
            edges {
                node {
                    dbId
                    assignmentDate
                    isHeaderApproved
                    headerApprovedAt
                    owner {
                        description
                        dbId
                    }
                    employee {
                        code
                        description
                        dbId
                    }
                    activity {
                        code
                        description
                    }
                    timeType {
                        code
                        description
                    }
                    workingHours
                    assignmentDate
                }
            }
            pageInfo {
                hasNextPage
            }
        }
    }
""")


GET_TIMESHEET_DELTAS = gql("""
    query getTimesheetDeltas($first: Int, $after: String) {
        timesheet_deltas(
            first: $first, 
            after: $after
        ) {
            edges {
                node {
                    dbId
                    modifiedAt
                    createdAt
                    approved
                    employeeDbId
                    mutationType
                    syncVersion
                    employee {
                        code
                        description
                        dbId
                    }
                    timeType {
                        code
                        description
                    }
                    workingHours
                    assignmentDate
                    _current {
                        dbId
                        approved
                        approvedAt
                        workingHours
                        assignmentDate
                        owner {
                            description
                            dbId
                        }
                        employee {
                            code
                            description
                            dbId
                        }
                        activity {
                            code
                            description
                        }
                        timeType {
                            code
                            description
                        }
                    }
                }
                mutationType
            }
            pageInfo {
                hasNextPage
            }
        }
    }
""")

MyQuery = gql("""
    query MyQuery {
        timesheet_deltas(first: 10000) {
            edges {
                mutationType
                node {
                    mutationType
                    dbId
                }
            }
        }
    }
""")
