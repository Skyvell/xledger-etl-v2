from gql import gql 


GET_TIMESHEETS_FROM_DBIDS = gql("""
    query getTimesheets($first: Int, $after: String, $dbIdList: [Int64String!]) {
        timesheets(
            first: $first,
            after: $after, 
            filter: { 
                dbId_in: $dbIdList
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
                    mutationType
                }
            }
            pageInfo {
                hasNextPage
            }
        }
    }
""")


GET_CUSTOMERS_FROM_DBIDS = gql("""
    query getCustomers($first: Int, $after: String, $dbIdList: [Int!]) {
        customers(
            first: $first, 
            after: $after, 
            filter: { dbId_in: $dbIdList }
        ) {
            edges {
                cursor
                node {
                    email
                    code
                    description
                    dbId
                    company {
                        name
                    }
                }
            }
            pageInfo {
                hasNextPage
            }
        }
    }
""")


GET_CUSTOMER_DELTAS = gql("""
    query getCustomerDeltas($first: Int, $after: String) {
        customer_deltas(
            first: $first, 
            after: $after
        ) {
            edges {
                node {
                    dbId
                    mutationType
                }
            }
            pageInfo {
                hasNextPage
            }
        }
    }
""")



#query MyQuery {
#  employees(first: 10000) {
#    edges {
#      cursor
#      node {
#        code
#        dbId
#        email
#        employmentType {
#          description
#          levelParent {
#            description
#          }
#        }
#        employeeGroup {
#          description
#          code
#        }
#        employmentTo
#        superior {
#          description
#        }
#        contact {
#          country {
#            description
#          }
#          gender {
#            name
#          }
#          name
#          lastName
#          exitReason {
#            description
#          }
#          jobTitle
#        }
#        employmentFrom
#        position {
#          dbId
#          createdAt
#          modifiedAt
#          dateFrom
#          dateTo
#          overtime
#          flextime
#          positionNumber
#          text
#          ownerDbId
#          seniorityDate
#          autoAdjustment
#          employeePositionNumber
#          seniorityAdjustments
#          comment
#          internalInfo
#          employmentComment
#          employeeDbId
#          parttimePct
#          mainPosition
#        }
#      }
#    }
#    pageInfo {
#      hasNextPage
#    }
#  }
#}
###
#query MyQuery {
#  customers(first: 10) {
#    edges {
#      cursor
#      node {
#        email
#        code
#        description
#        dbId
#        company {
#          name
#        }
#      }
#    }
#  }
#}
#
#customer.name : customer_name_db_1
#customer_name_db_1 : customer_name_db_2